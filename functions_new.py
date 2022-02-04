from sqlalchemy import column
import streamlit as st
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import NMF
import plotly.graph_objects as go

from config import dropdown


# relative path
PATH = os.path.abspath('')


# loading ratings data
@st.cache(show_spinner=False)
def load_ratings():
    df_ratings = pd.read_csv(PATH + os.sep + 'data/ratings.csv')
    return df_ratings


# loading movies data
@st.cache(show_spinner=False)
def load_movies():
    df_movies = pd.read_csv(PATH + os.sep + 'data/movies.csv')
    df_movies.drop_duplicates(subset="title", keep='first', inplace=True)
    return df_movies


# Merging ratings and movies datasets, dropping the columns we dont need,
@st.cache(show_spinner=False)
def merging_df(df_ratings, df_movies):
    df_merged = pd.merge(df_movies, df_ratings, on='movieId', how='right')
    df_merged.drop(columns=['timestamp', 'genres', 'movieId'], inplace=True)
    return df_merged 


# Dropping movies under 20 ratings
def dropping_movies(df_merged, df_movies, df_ratings):
    df_agg = df_merged.groupby(['title'])['rating'].agg(['mean', 'count'])
    df_dropped = df_agg.loc[df_agg['count'] > 20].reset_index()
    df1 = pd.merge(df_movies, df_dropped, on='title', how='right')
    df1.drop(columns=['genres', 'mean', 'count'], inplace=True)
    df_merged = pd.merge(df_ratings, df1, on='movieId', how='right')
    df_merged.drop(columns=['timestamp'], inplace=True)
    return df1, df_merged
    

# list of movies for submit form
@st.cache(show_spinner=False, allow_output_mutation=True)
def get_movies_list(df_merged):
    df_drop = df_merged[df_merged['title'].isna()]
    df_dropped = df_merged.drop(df_drop.index, axis=0)
    df_sorted = df_dropped.sort_values(by=['title'], ascending=True)
    movies_list = df_sorted['title'].unique().tolist()
    movies_list = [''] + movies_list
    return movies_list


# insert a row into df_user
def insert_input(df_user, movie_select, rating_select): 
    df_user = df_user.append({'title': movie_select, 'rating': rating_select}, ignore_index=True)
    df_user.index = df_user.index + 1
    return df_user

def remove_last(df_user):
    df_user.drop(df_user.tail(1).index, inplace=True)
    return df_user


# def plotly_table(df_user):
#     fig = go.Figure(data=[go.Table(
#     header=dict(values=list(df_user.columns),
#                 fill_color='paleturquoise',
#                 align='left'),
#     cells=dict(values=[df_user.Movie, df_user.Rating],
#                fill_color='lavender',
#                align='left'))
#     ])
#     return fig


# remove number column and add +1 to indux 
def remove_number(df_user): 
    df_user = df_user.drop(columns=['number'])
    df_user.index = df_user.index + 1
    return df_user


# creating dataframe with user-user cosine similarity matrix, transposing dataframe, users to columns, movies to index
def cosim_matrix(df_merged):
    df_cosim = df_merged.pivot_table(values='rating', index='userId', columns='title')
    df_cosim = df_cosim.fillna(value=2.5)
    df_cosim = pd.DataFrame(cosine_similarity(df_cosim)).round(3)
    return df_cosim


# non negative matrix factorization
def nmf_recommender(df_user, df_merged, df1): 

    # user input 
    df_user = df_user.pivot_table(values='rating', columns='title')

    # Creating user_rating-movie matrix, filling nan with mean in the row of the user
    mx = df_merged.pivot_table(index='userId', columns='title', dropna=False, values='rating')
    mx.fillna(mx.mean(), inplace=True)

    # appending df_user to matrix in the last row 
    mx_appended = mx.append(df_user) 
    mx_appended = mx_appended.rename({'rating': 'new_user'}, axis='index')

    # user row which we need to nmf.model.transform, nan filled with mean of matrix
    mx_user = pd.DataFrame(mx_appended.loc['new_user']).T
    mx_user.fillna(mx.mean(), inplace=True)

    # nmf model
    nmf_model = NMF(n_components=200, max_iter=200)
    R = mx.values
    nmf_model.fit(R) 
    Q = nmf_model.components_ 
    P_user = nmf_model.transform(mx_user)
    predictions = np.dot(P_user, Q)
    
    # remove already rated items

    df_predictions = pd.DataFrame(df1)
    df_predictions['predicted_rating'] = predictions[0] 

    # movies seen by new user, rearranging the dataframe to original
    df_user = pd.DataFrame(df_user.T.reset_index()) 

    # adding a column of already rated movies by (merging df_user dataframe)
    df_recommend = pd.merge(df_predictions, df_user, on='title', how='outer')

    # removing movies which were already rated by the user
    df_recommend = df_recommend[df_recommend['rating'].isnull()]
    df_recommend = df_recommend.sort_values(by='predicted_rating', ascending=False).head(20) 
    return df_recommend



def nbcf_recommender(df_user, df_merged): 

    # user input
    df_user = df_user.pivot_table(values='rating', columns='title')
    
    # ratings movie matrix
    mx = df_merged.pivot_table(values='rating', columns='title', index='userId')
    mx.fillna(mx.mean(), inplace=True)
    # mx.fillna(value=0, inplace=True) 
    # mx.fillna(value=2.5, inplace=True) 

    # appending df_user to matrix in the last row 
    mx_appended = mx.append(df_user)
    #mx_appended.fillna(value=0, inplace=True)
    mx_appended.fillna(mx.mean(), inplace=True)  
 
    # cosine similarity matrix
    mx_cosim = pd.DataFrame(cosine_similarity(mx_appended))

    # selecting user column from cosine similarity matrix
    df_user_cosim = pd.DataFrame(mx_cosim.iloc[:, [-1]])

    # renaming column
    df_user_cosim = df_user_cosim.rename({df_user_cosim.columns.values[0]: 'new_user'}, axis=1)

    # creating a list of similar users
    df_similar_users = df_user_cosim.sort_values(by='new_user', ascending=False).head(11)
    df_similar_users = df_similar_users.iloc[1: , :]
    similar_users = list(df_similar_users.index)

    # matrix of ratings of similar users 
    mx_similar_users = mx.loc[similar_users]

    # numerator
    num = np.dot(df_similar_users.T, mx_similar_users)

    # denominator
    df_rating_count = mx_similar_users.where(mx_similar_users == 0, 1)                                    
    denom = np.dot(df_similar_users.T, df_rating_count)

    # predicting ratings 
    predictions = num/denom
    df_predictions = pd.DataFrame(predictions.T, columns=["predicted_ratings"])

    # recommendations
    df_movies2 = df_rating_count.T.reset_index()
    df_movies2 = pd.DataFrame(df_movies2['title'])
    df_recommendation = df_movies2.join(df_predictions).set_index('title')

    # removing movies which were rated under 20 times, 
    # in case if fillna is 2.5 or mean
    count = pd.DataFrame(np.sum(df_rating_count, axis=0)).reset_index()
    count.rename(columns={0 : 'count'}, inplace=True)
    df_recommendation = pd.merge(df_recommendation, count, on='title')
    df_recommendation = df_recommendation.loc[df_recommendation['count'] > 1].sort_values(by='predicted_ratings', ascending=False)
    
    # match % set to index, 
    df_recommendation.rename(columns={'predicted_ratings': 'match (%)'}, inplace=True)
    df_recommendation['match (%)'] = df_recommendation['match (%)'] * 20
    df_recommendation['match (%)'] = df_recommendation['match (%)'].astype(int)
    df_recommendation['match (%)'] = df_recommendation['match (%)'].astype(str) + ' %'
    df_recommendation.set_index('match (%)', inplace=True)
    df_recommendation.drop(columns=['count'], inplace=True)
    
    # dropping movies that the user has already seen
    #df_user_nan = df_user.loc[df_user['new_user'].isnull()]

    return df_recommendation



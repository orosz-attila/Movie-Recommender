import pandas as pd
import streamlit as st
import sqlalchemy
import urllib.parse


# connecting to postgres 'recommender' database 
@st.cache(allow_output_mutation=True)
def connect_engine():
    engine = sqlalchemy.create_engine("postgresql://postgres:postgres@localhost:5432/recommender")
    return engine

# try after create_engine st.secrets["postgres"]

# creating sql table for user input 
st.cache(hash_funcs={sqlalchemy.engine.base.Engine: id})
def create_table(engine):
    query = '''
    CREATE TABLE IF NOT EXISTS df_user (
        number SERIAL,
        title VARCHAR(500),
        rating INT
    );
    '''
    engine.execute(query)
    return  

# insert new row with user input from the submit form into sql table  
st.cache(hash_funcs={sqlalchemy.engine.base.Engine: id})
def insert_data(engine, movie_select, rating_select):
    query = "INSERT INTO df_user (title, rating) VALUES (%s, %s);"
    engine.execute(query, (movie_select, rating_select)) 
    return 


# removing last row from sql table 
st.cache(hash_funcs={sqlalchemy.engine.base.Engine: id})
def remove_last_row(engine):
    query = "DELETE FROM df_user WHERE ctid IN (SELECT ctid FROM df_user ORDER BY number LIMIT 1);"
    engine.execute(query) 
    return 


# get date from postgres and load it into a pandas dataframe  
st.cache(hash_funcs={sqlalchemy.engine.base.Engine: id})
def get_data(engine):
    query = """
    SELECT * FROM df_user;
    """
    df_user = pd.read_sql(query, con=engine)
    return df_user 


# reset button: emptying sql table
st.cache(hash_funcs={sqlalchemy.engine.base.Engine: id}) 
def empty_table(engine):
    query = '''
    DELETE FROM df_user;
    '''
    engine.execute(query)
    return 
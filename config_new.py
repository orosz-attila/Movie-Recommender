import streamlit as st
import pandas as pd
import urllib.parse
import random
import time

import os
PATH = os.path.abspath('')


# setting page config
def page_config():
    st.set_page_config(
        page_title="Movie Recommender",
        layout="centered"
        #page_icon=PATH + os.sep + 'data/.png',
    )


# def alert():
#     st.markdown('<div class="stAlert" style="margin-top: 500px;" </div>', unsafe_allow_html=True)



def dropdown():
    st.markdown(
        """
    <style>
    .css-1d0tddh {
        text-overflow: clip;
        overflow: revert;
        white-space: nowrap;
    }
    </style>    
    """,
        unsafe_allow_html=True,
    )


def random_gif():
    gif_list = ['https://64.media.tumblr.com/tumblr_ldbj01lZiP1qe0eclo1_500.gifv', 
                'https://25.media.tumblr.com/tumblr_m9ldt94Vmx1rzhs87o1_400.gifv',
                'https://64.media.tumblr.com/tumblr_lc738lDRh31qe0eclo1_r1_500.gifv',
                'https://64.media.tumblr.com/tumblr_lg5v1v555R1qe0eclo1_r2_500.gifv', 
                'https://64.media.tumblr.com/cbc95d977b80b456100225ea0045abef/tumblr_lvkqenqVfH1qe0eclo1_r23_500.gifv',
                'https://64.media.tumblr.com/67d5f672a4a3d86a97d863f28688be28/tumblr_nxt51r9wl81qe0eclo2_r1_500.gifv',
                'https://64.media.tumblr.com/tumblr_laonjuZpOg1qe0eclo1_r4_500.gifv',
                'https://64.media.tumblr.com/tumblr_lasmpzzeeO1qe0eclo1_r2_500.gifv',
                'https://64.media.tumblr.com/tumblr_lce2v5RdkQ1qe0eclo1_r3_500.gifv',
                'https://64.media.tumblr.com/e143caf373a57a149f7d0ce7d4d461e2/tumblr_ldsq207kj41qe0eclo2_r1_500.gifv',
                'https://64.media.tumblr.com/tumblr_lf0civt0Fh1qe0eclo1_r2_500.gifv',
                ]
    n = random.randint(0,10)
    url = gif_list[n]
    #print('Function random_gif', n, url)
    return url


def background(url):
    st.markdown(
        f'''
    <style>
    .main {{
        background-image: url({url});
        background-size: cover;
        background-position-x: center;
        opacity: 90%;
    }}
    </style>
    ''',  
    unsafe_allow_html=True,
    )


# setting sidebar css
def sidebar():
   st.markdown(
    """
    <style>
    .css-ng1t4o {
        padding: 1rem;
    }
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -500px;
    }
    .css-zuelfj {
        margin-top: 0px;
        margin-bottom: 0px;
    }
    ''',
    </style>
    """,
    unsafe_allow_html=True,
)

def footer(): 
    st.markdown("""
    <style>
    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def container():
    st.markdown(
        """
    <style>
    .css-1v3fvcr {
        position: relative;
        flex-direction: column;
        overflow: auto;
    }
    .reportview-container .main .block-container{
        max-width: 100%;
        padding-top: 1rem;
        padding-left: 0rem;
        padding-right: 0rem;
        padding-bottom: 0rem;
    }
    </style>    
    """,
        unsafe_allow_html=True,
    )

def header_1():
    st.markdown(
        """
    <style>
    .css-ng1t4o h1 {
        font-size: 60px;
        padding: 0;
        text-align: left;
        color: rgb(229, 9, 20);
        font-weight: 700;
        margin-top: -10px;
    }
    </style>    
    """,
        unsafe_allow_html=True,
    )

# def title(title):
#     st.markdown(f'<h1 style="padding: 1rem; font-size: 60px; padding: 0; text-align: left; color: rgb(229, 9, 20); font-weight: 700;">{title}</h1>', unsafe_allow_html=True)


def header_2():
    st.markdown(
        """
    <style>
    .css-ng1t4o h2 {
        color: white;
        font-size: 24px;
        font-weight: 600;
        text-align: left;
        padding-top: 0px;
        padding-bottom: 16px;
    }
    </style>    
    """,
        unsafe_allow_html=True,
    )


def select_box():
    st.markdown(
        """
    <style>

    .block-container {
        padding: 0rem;
    }
    .css-16huue1 {
        background: rgb(19, 23, 32) none repeat scroll 0% 0%;
        width: fit-content;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 0.4rem;
        padding-top: 0.4rem;
    }
    .css-slr766 {
        
    }
     </style>    
    """,
        unsafe_allow_html=True,
    )


def warning():
    st.markdown(
        """
    <style>
    p {
        color: white;
        font-size: 24px;
        font-weight: 600;
        text-align: center;
    }    
    """,
        unsafe_allow_html=True,
    )
    

def column_buttons():
    st.markdown(
        """
    <style>
    .css-keje6w {
        text-align: center;
    }    
    """,
        unsafe_allow_html=True,
    )


def expander_html():
    st.write(
        """
    <p style='text-align: justify; font-size: 1rem; font-weight: 400; padding: 0px; margin: 0px 0px 1rem;'>Select a movie from the dropdown menu and rate it on a scale from 1 to 5. Add at least 10 movies, finally hit 'Recommend' below.
    </p>""", 
    unsafe_allow_html=True,
    )
import streamlit as st
import gspread
import pandas as pd
import sqlite3

DB_NAME = "grievances.db"

def get_all_grievances():
    with sqlite3.connect(DB_NAME) as conn:
        return pd.read_sql_query(
            '''SELECT 
                   title, 
                   message AS "What's on your mind?", 
                   mood AS "Current Mood", 
                   date AS "Date" 
               FROM grievances 
               ORDER BY date DESC''', 
            conn
        )
st.title('Thank you')
st.write('Your grievance has been sent to Jason. He will take a look at it aaram se')
from google.oauth2.service_account import Credentials
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
]
skey = st.secrets['gcp_service_account']
credentials = Credentials.from_service_account_info(
    skey,
    scopes=scopes,
)

client1 = gspread.authorize(credentials)
sht = client1.open_by_url('https://docs.google.com/spreadsheets/d/1sBZaGwnssN4tLbuyYYoYFWrvDw0wG2VNDCXoLS_8tGk/edit?usp=sharing')
worksheet = sht.worksheet('Sheet1')

if st.button(label='View your past entries'):
    df = get_all_grievances()
    st.dataframe(df)


if st.button(label='Make a New Entry'):
    st.switch_page('pages/portal.py')
import streamlit as st
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

if st.button(label='View your past entries'):
    df = get_all_grievances()
    st.dataframe(df)


if st.button(label='Make a New Entry'):
    st.switch_page('pages/portal.py')
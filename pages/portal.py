import google.genai
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import google
from google.genai import types

# --- Database Setup ---
DB_NAME = "grievances.db"

def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                mood TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_grievance(title, message, mood, date):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT INTO grievances (title, message, mood, date)
            VALUES (?, ?, ?, ?)
        ''', (title, message, mood, date))
        conn.commit()

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
# --- Session State Initialization ---
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False
if 'show_message' not in st.session_state:
    st.session_state['show_message'] = False

# --- Create DB Table ---
create_table()

# --- Streamlit UI ---
st.title('Grievance Portal')

title = st.text_input(label='Title')
bothering_message = st.text_input(label="What's on your mind?")
option = st.selectbox('Choose your current mood', ('😀','🥰', '😡', '🥺'), index=None)

# --- Submit Logic ---
if title and bothering_message and option:
    if st.button(label='Submit'):
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_grievance(title, bothering_message, option, current_datetime)
        st.session_state['submitted'] = True
        st.success("Entry submitted successfully!")

# --- Generate Gemini AI Message ---
if st.session_state['submitted']:
    if st.button(label='Collect your special message'):
        st.session_state['show_message'] = True

if st.session_state['show_message']:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = google.genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            system_instruction="You are a supportive friend. You will write sweet and kind messages to the user who is grieving or troubled. Do not call her honey"
        ),
        contents=bothering_message
    )
    st.text_area(label='Your special message:', value=response.text, height=200)

# --- View Past Entries ---
if st.button(label='Proceed'):
    st.switch_page('pages/portal.py')

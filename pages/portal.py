import streamlit as st
import gspread
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

from datetime import datetime
import pandas as pd
from google import genai
from google.genai import types


api_key = st.secrets["GEMINI_API_KEY"]

sht = client1.open_by_url('https://docs.google.com/spreadsheets/d/1sBZaGwnssN4tLbuyYYoYFWrvDw0wG2VNDCXoLS_8tGk/edit?usp=sharing')
worksheet = sht.worksheet('Sheet1')

# Initialize session state to track submission
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False
if 'show_message' not in st.session_state:
    st.session_state['show_message'] = False

def submit_value(title, bothering_message, option):
    existing_df = pd.DataFrame(worksheet.get_all_records())
    current_datetime = datetime.now()
    new_data = pd.DataFrame([{
        "Title": title,
        "What's on your mind?": bothering_message,
        'Current Mood': option,
        "Date": current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    }])

    updated_df = pd.concat([existing_df, new_data], ignore_index=True)
    updated_df["Date"] = pd.to_datetime(updated_df["Date"], errors='coerce')
    updated_df = updated_df.sort_values(by="Date", ascending=False)
    data = [updated_df.columns.tolist()] + updated_df.astype(str).values.tolist()
    worksheet.update('A1', data)

    st.session_state['submitted'] = True
    st.success("Entry submitted successfully!")

st.title('Grievance Portal')

title = st.text_input(label='Title')
bothering_message = st.text_input(label="What's on your mind?")
option = st.selectbox('Choose your current mood', ('😀','🥰', '😡', '🥺'), index=None)

if title and bothering_message and option:
    if st.button(label='Submit'):
        submit_value(title, bothering_message, option)

if st.session_state['submitted']:
    if st.button(label='Collect your special message'):
        st.session_state['show_message'] = True


if st.session_state['show_message']:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        config=types.GenerateContentConfig(
            system_instruction="You are a supportive boyfriend. You will write sweet and kind messages to the user who is grieving or troubled. Do not call her honey. Call her things like 'Sweetheart', 'Kuchupuchu', Babygirl, 'Lovey', 'Sweet girl'."
        ),
        contents=bothering_message
    )
    st.text_area(label='Your special message:', value=response.text, height=300)
    if st.button('Proceed'):
            st.switch_page('pages/ending.py')

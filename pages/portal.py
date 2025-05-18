import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
from datetime import datetime
import pandas as pd
from google import genai
from google.genai import types

import telebot
BOT_TOKEN = st.secrets['BOT_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)

api_key = st.secrets["GEMINI_API_KEY"]
conn = st.connection("gsheets", type=GSheetsConnection)

# Initialize session state to track submission
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False
if 'show_message' not in st.session_state:
    st.session_state['show_message'] = False

# def submit_value(title, bothering_message, option):
#     existing_df = conn.read(worksheet='Sheet1',
#                             usecols=[0, 1, 2, 3])
#     current_datetime = datetime.now()
#     new_data = pd.DataFrame([{
#         "Title": title,
#         "What's on your mind?": bothering_message,
#         'Current Mood': option,
#         "Date": current_datetime.strftime('%Y-%m-%d %H:%M:%S')
#     }])

#     updated_df = pd.concat([existing_df, new_data], ignore_index=True)
#     updated_df["Date"] = pd.to_datetime(updated_df["Date"], errors='coerce')
#     updated_df = updated_df.sort_values(by="Date", ascending=False)
#     conn.update(worksheet='Sheet1', data=updated_df)

#     st.session_state['submitted'] = True
#     st.success("Entry submitted successfully!")

st.title('Grievance Portal')

title = st.text_input(label='Title')
bothering_message = st.text_input(label="What's on your mind?")
option = st.selectbox('Choose your current mood', ('😀','🥰', '😡', '🥺'), index=None)

if title and bothering_message and option:
    if st.button(label='Submit'):
        st.session_state['submitted'] = True
        message = f"📬 *New Submission Received:*\n\n*Title:* {title}\n*Message:* {bothering_message}\n*Option:* {option}"
        bot.send_message(chat_id='t.me/Grievance_port_bot', text=message, parse_mode='Markdown')


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

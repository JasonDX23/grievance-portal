import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

st.title('Thank you')
st.write('Your grievance has been sent to Jason. He will take a look at it aaram se')
from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection)

if st.button(label='View your past entries'):
    existing_df = conn.read(worksheet='Sheet1', usecols=[0, 1, 2, 3])
    st.dataframe(existing_df)

if st.button(label='New Entry'):
    st.switch_page('pages/portal.py')
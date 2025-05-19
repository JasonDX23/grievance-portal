import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)


st.title('Grievance Portal')
st.markdown('As requested, you can submit your grievances for my viewing pleasure')


if st.button(label='Access your portal'):
    st.switch_page('pages/portal.py')





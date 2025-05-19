import streamlit as st


st.title('Grievance Portal')
st.markdown('As requested, you can submit your grievances for my viewing pleasure')


if st.button(label='Access your portal'):
    st.switch_page('pages/portal.py')





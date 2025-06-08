# modules/utils.py
import streamlit as st

def set_session_user(user):
    st.session_state['user'] = user

def get_session_user():
    return st.session_state.get('user', None)

def clear_session_user():
    if 'user' in st.session_state:
        del st.session_state['user']

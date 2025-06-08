# config/db_config.py
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

def get_connection():
    if 'db_conn' not in st.session_state:
        conn = psycopg2.connect(
            host="localhost",
            database="AirportFlightManagement",
            user="yasir",
            password="yasir1234",
            port=6677
        )
        st.session_state['db_conn'] = conn
    return st.session_state['db_conn']

def get_cursor():
    """Returns just the cursor (for backward compatibility)"""
    conn = get_connection()
    return conn.cursor(cursor_factory=RealDictCursor)

def get_cursor_and_connection():
    """Returns both cursor and connection"""
    conn = get_connection()
    return conn.cursor(cursor_factory=RealDictCursor), conn
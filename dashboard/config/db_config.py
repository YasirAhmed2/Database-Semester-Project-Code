import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# ---------------------------------------
# DB CONFIGURATION
# ---------------------------------------

def get_db_connection():
    """
    Establish and return a PostgreSQL connection.
    Update your credentials as needed.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="AirportFlightManagement",
            user="yasir",
            password="yasir1234",
            port="6677",
            cursor_factory=RealDictCursor  # Optional: fetch results as dicts
        )
        return conn
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

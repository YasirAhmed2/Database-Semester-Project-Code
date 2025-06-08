# login.py

import streamlit as st
import psycopg2
from auth.auth_utils import get_user_by_email_and_role, check_password

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="AirportFlightManagement",
        user="yasir",
        password="yasir1234",
        port="6677"
    )

def authenticate_user(email: str, password: str, role: str):
    if not email or not password or not role:
        return None

    conn = None
    try:
        conn = connect_db()
        user = get_user_by_email_and_role(conn, email, role)
        if user and check_password(password, user['hashed_password']):
            return user
        else:
            return None
    except Exception as e:
        st.error(f"Error during authentication: {e}")
        return None
    finally:
        if conn:
            conn.close()

def login_screen():
    st.title("✈️ Airport Management Login")

    roles = ["Admin", "Pilot", "Security Officer", "Customer", "Airline Staff"]
    selected_role = st.selectbox("Select Role", roles)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
            return None

        user = authenticate_user(email, password, selected_role)
        if user:
            st.success(f"Welcome, {user['name']}! You are logged in as {user['role']}.")
            return user
        else:
            st.error("Invalid email, password, or role.")
            return None

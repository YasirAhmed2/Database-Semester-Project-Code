import streamlit as st
import psycopg2
from auth_utils import get_user_by_email, check_password

# -------------- #
# DB CONNECTION  #
# -------------- #
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="AirportFlightManagement",
        user="yasir",
        password="yasir1234",
        port="6677"  # adjust if necessary
    )

# ---------------------------- #
# STREAMLIT LOGIN UI & LOGIC  #
# ---------------------------- #
def login_screen():
    st.title("✈️ Airport Management Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        conn = connect_db()
        user = get_user_by_email(conn, email)

        if user and check_password(password, user['hashed_password']):
            st.success(f"Welcome, {user['name']}! Logged in as {user['role']}")

            # Set session state
            st.session_state.logged_in = True
            st.session_state.user_id = user['user_id']
            st.session_state.name = user['name']
            st.session_state.email = user['email']
            st.session_state.role = user['role']
        else:
            st.error("Invalid email or password.")

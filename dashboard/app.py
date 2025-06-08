import streamlit as st
# from auth.login import login_screen # Your login function returning user dict or None
from utils.ui_components import show_header, show_error, show_success, button
from auth.login import authenticate_user

# Import role-based UI modules (you would implement these separately)
from crud import admins
from crud import passengers
# from crud import pilots
# from crud import airline_staff
# from crud import security_officers

def main():
    st.set_page_config(page_title="Airport Management System", page_icon="✈️", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user = None

    if not st.session_state.logged_in:
        show_login()
    else:
        show_dashboard()

def show_login():
    show_header("Airport Management System Login", icon="🔐")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            show_success(f"Welcome {user['full_name']}! You are logged in as {user['role']}.")
            st.experimental_rerun()
        else:
            show_error("Invalid credentials. Please try again.")

def show_dashboard():
    user = st.session_state.user
    role = user.get("role")

    st.sidebar.write(f"👤 Logged in as: {user.get('full_name')} ({role})")
    if button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.experimental_rerun()

    if role == "admin":
        admins.show_admin_dashboard()
    elif role == "passenger":
        passengers.show_passenger_dashboard()
    elif role == "pilot":
        pilots.show_pilot_dashboard()
    elif role == "airline_staff":
        airline_staff.show_airline_staff_dashboard()
    elif role == "security_officer":
        security_officers.show_security_officer_dashboard()
    else:
        st.error("Role not recognized. Contact administrator.")

if __name__ == "__main__":
    main()

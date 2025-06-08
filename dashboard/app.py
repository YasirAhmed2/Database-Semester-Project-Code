# app.py
import streamlit as st
from modules.auth import get_roles, validate_login
from modules.utils import set_session_user, get_session_user, clear_session_user
from modules.dashboards import load_dashboard

def login_page():
    st.title("Airport Management System - Login")
    
    roles = get_roles()
    role_dict = {r['role_name']: r['role_id'] for r in roles}
    selected_role = st.selectbox("Select Role", list(role_dict.keys()))
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    
    if login_btn:
        role_id = role_dict[selected_role]
        user = validate_login(email, password, role_id)
        if user:
            st.success(f"Logged in as {user['full_name']} ({selected_role})")
            set_session_user(user)
            st.rerun()
        else:
            st.error("Invalid credentials or role mismatch.")

def logout():
    clear_session_user()
    st.rerun()

def main():
    user = get_session_user()
    if user:
        st.sidebar.write(f"Logged in as: {user['full_name']}")
        if st.sidebar.button("Logout"):
            logout()
        load_dashboard(user)
    else:
        login_page()

if __name__ == "__main__":
    main()

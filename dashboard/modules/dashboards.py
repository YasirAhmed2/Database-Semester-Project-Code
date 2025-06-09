# modules/dashboards.py
import streamlit as st
from modules.super_admin import dashboard
from modules.flight_manager import flight_manager_dashboard
def load_dashboard(user):
    role_id = user['role_id']
    
    # For demonstration, let's just print role_id and user info
    st.header("Dashboard")
    st.write(f"Welcome, {user['full_name']}!")
    # st.write(f"Role ID: {role_id}")

    # Here you will add role-specific dashboards, e.g.:
    if role_id == 1:  # SuperAdmin (example)
        st.write("Super Admin")
        dashboard()
        # call functions to show admin dashboard
    elif role_id == 2:  # Manager
        st.write("Flight Manager")
        flight_manager_dashboard()
        # pilot_dashboard(user)

    else:
        st.write("Role dashboard not implemented yet.")

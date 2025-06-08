# modules/dashboards.py
import streamlit as st
from modules.admin_dashboard import admin_dashboard
from modules.security_officer import security_officer_dashboard
from modules.pilot_dashboard import pilot_dashboard
def load_dashboard(user):
    role_id = user['role_id']
    
    # For demonstration, let's just print role_id and user info
    st.header("Dashboard")
    st.write(f"Welcome, {user['full_name']}!")
    # st.write(f"Role ID: {role_id}")

    # Here you will add role-specific dashboards, e.g.:
    if role_id == 1:  # SuperAdmin (example)
        st.write("Admin Dashboard")
        admin_dashboard()
        # call functions to show admin dashboard
    elif role_id == 2:  # Manager
        st.write("Pilot Dashboard")
        pilot_dashboard(user)
    elif role_id == 3:  # Staff
        st.write("Airline staff Dashboard")
    elif role_id == 4:  # Passenger (if role exists)
        st.write("Security Officer Dashboard")
        security_officer_dashboard(user)

    else:
        st.write("Role dashboard not implemented yet.")

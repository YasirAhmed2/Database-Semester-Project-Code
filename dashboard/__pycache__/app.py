import streamlit as st
from auth import authenticate_user, get_user_role
from db.db import get_db
from db.crud import crud

# --- Login Section ---
st.set_page_config(page_title="Airport Management System", layout="wide")
st.title("✈️ Airport Management Dashboard")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

if not st.session_state.authenticated:
    with st.form("login_form"):
        st.subheader("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            db = next(get_db())
            user = authenticate_user(db, email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.role = get_user_role(user)
                st.success(f"Logged in as {st.session_state.role}")
            else:
                st.error("Invalid email or password")
    st.stop()

# --- Role-Based Views ---
role = st.session_state.role

def passenger_view():
    st.header("🧳 Passenger Dashboard")
    st.write("View your bookings and flight details here.")
    # TODO: Add passenger-specific CRUD

def staff_view():
    st.header("🛫 Airline Staff Dashboard")
    st.write("Manage flights, gates, and terminals.")
    # TODO: Add flight, airport, gate, terminal management

def pilot_view():
    st.header("🧑‍✈️ Pilot Dashboard")
    st.write("View your assigned flight schedules.")
    # TODO: Add read-only view of assigned schedules

def security_view():
    st.header("🛂 Security Officer Dashboard")
    st.write("Access passenger verification and flight status logs.")
    # TODO: Add passenger lookup & flight logs

role_view_map = {
    "Passenger": passenger_view,
    "Manager": staff_view,
    "SuperAdmin": staff_view,
    "Staff": staff_view,
    "Pilot": pilot_view,
    "Security": security_view
}

if role in role_view_map:
    role_view_map[role]()
else:
    st.error("Role not recognized. Contact Admin.")

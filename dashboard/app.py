import streamlit as st
from auth.login import login_user
from crud import airports, passengers, bookings, flights, admins
from config.db_config import init_connection

# Initialize DB connection
conn = init_connection()

# Set page config
st.set_page_config(page_title="✈️ Airline Management", layout="wide")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'admin_id' not in st.session_state:
    st.session_state.admin_id = None

# Login
if not st.session_state.logged_in:
    st.title("🔐 Airline Management System")
    st.subheader("Please log in to continue")

    success = login_user(conn)
    if not success:
        st.stop()

# Sidebar Navigation
st.sidebar.title("📋 Menu")

role = st.session_state.role

if role == "SuperAdmin":
    menu = st.sidebar.radio("Select Panel", ["Airports", "Flights", "Passengers", "Bookings", "Admins"])
    if menu == "Airports":
        airports.render_airports_ui(conn)
    elif menu == "Flights":
        flights.render_flights_ui(conn)
    elif menu == "Passengers":
        passengers.render_passengers_ui(conn)
    elif menu == "Bookings":
        bookings.render_bookings_ui(conn)
    elif menu == "Admins":
        admins.render_admins_ui(conn)

elif role == "Manager" or role == "Airline Staff":
    menu = st.sidebar.radio("Select Panel", ["Flights", "Passengers", "Bookings"])
    if menu == "Flights":
        flights.render_flights_ui(conn)
    elif menu == "Passengers":
        passengers.render_passengers_ui(conn)
    elif menu == "Bookings":
        bookings.render_bookings_ui(conn)

elif role == "Security Officer":
    menu = st.sidebar.radio("Select Panel", ["Passenger Details", "Flight Info"])
    if menu == "Passenger Details":
        passengers.render_passengers_ui(conn, read_only=True)
    elif menu == "Flight Info":
        flights.render_flights_ui(conn, read_only=True)

elif role == "Pilot":
    st.subheader("🧑‍✈️ Pilot Dashboard")
    flights.render_flights_ui(conn, pilot_view=True)

elif role == "Passenger":
    menu = st.sidebar.radio("Select Panel", ["My Bookings", "Flight Schedules"])
    if menu == "My Bookings":
        bookings.render_passenger_bookings_ui(conn)
    elif menu == "Flight Schedules":
        flights.render_passenger_schedule_ui(conn)

else:
    st.warning("❌ Unknown role. Please contact administrator.")

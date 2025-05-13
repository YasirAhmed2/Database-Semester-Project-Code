import streamlit as st
import psycopg2
from psycopg2 import sql
from datetime import datetime
import pandas as pd

# Database connection function with error handling
def get_connection():
    try:
        conn = psycopg2.connect(
            dbname="AirportFlightManagement",
            user="yasir",
            password="yasir1234",
            host="localhost",
            port="6677"
        )
        return conn
    except psycopg2.Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Initialize connection
conn = get_connection()

# Helper function to execute queries with better error handling
def execute_query(query, params=None, fetch=False):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch:
                if query.strip().upper().startswith('SELECT'):
                    columns = [desc[0] for desc in cursor.description]
                    data = cursor.fetchall()
                    return pd.DataFrame(data, columns=columns) if data else pd.DataFrame()
                else:
                    return cursor.fetchone()
            conn.commit()
    except psycopg2.Error as e:
        st.error(f"Database error: {e}")
        conn.rollback()
        return None

# Page configuration
st.set_page_config(layout="wide", page_title="Flight Management System")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Airports", "Terminals", "Gates", 
    "Flight Statuses", "Payment Methods", "Booking Statuses",
    "Passengers", "Flights", "Flight Schedules",
    "Bookings", "Payments", "Admin Roles", "Admins", "Notifications"
])

# CRUD functions for each table
def manage_airports():
    st.title("Airports Management")
    
    # CRUD Operations
    operation = st.selectbox("Operation", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        with st.form("create_airport"):
            name = st.text_input("Name")
            city = st.text_input("City")
            country = st.text_input("Country")
            code = st.text_input("Code").upper()
            
            if st.form_submit_button("Create"):
                if not all([name, city, country, code]):
                    st.error("All fields are required!")
                else:
                    query = "INSERT INTO airports (name, city, country, code) VALUES (%s, %s, %s, %s) RETURNING airport_id"
                    result = execute_query(query, (name, city, country, code), fetch=True)
                    if result is not None:
                        st.success(f"Airport created with ID: {result.iloc[0][0]}")
    
    elif operation == "Read":
        query = "SELECT * FROM airports"
        df = execute_query(query, fetch=True)
        if df is not None:
            st.dataframe(df)
    
    elif operation == "Update":
        query = "SELECT airport_id, name FROM airports"
        airports = execute_query(query, fetch=True)
        if airports is not None and not airports.empty:
            airport_options = {row['name']: row['airport_id'] for _, row in airports.iterrows()}
            selected_airport = st.selectbox("Select Airport", options=list(airport_options.keys()))
            
            with st.form("update_airport"):
                query = "SELECT * FROM airports WHERE airport_id = %s"
                airport_data = execute_query(query, (airport_options[selected_airport],), fetch=True)
                if airport_data is not None and not airport_data.empty:
                    airport_data = airport_data.iloc[0]
                    
                    name = st.text_input("Name", value=airport_data['name'])
                    city = st.text_input("City", value=airport_data['city'])
                    country = st.text_input("Country", value=airport_data['country'])
                    code = st.text_input("Code", value=airport_data['code'])
                    
                    if st.form_submit_button("Update"):
                        query = "UPDATE airports SET name = %s, city = %s, country = %s, code = %s WHERE airport_id = %s"
                        execute_query(query, (name, city, country, code, airport_options[selected_airport]))
                        st.success("Airport updated successfully")
    
    elif operation == "Delete":
        query = "SELECT airport_id, name FROM airports"
        airports = execute_query(query, fetch=True)
        if airports is not None and not airports.empty:
            airport_options = {row['name']: row['airport_id'] for _, row in airports.iterrows()}
            selected_airport = st.selectbox("Select Airport to Delete", options=list(airport_options.keys()))
            
            if st.button("Delete"):
                # Check for dependencies first
                query = "SELECT COUNT(*) FROM terminals WHERE airport_id = %s"
                terminal_count = execute_query(query, (airport_options[selected_airport],), fetch=True)
                if terminal_count is not None:
                    terminal_count = terminal_count.iloc[0][0]
                    
                    if terminal_count > 0:
                        st.error("Cannot delete airport with associated terminals. Delete terminals first.")
                    else:
                        query = "DELETE FROM airports WHERE airport_id = %s"
                        execute_query(query, (airport_options[selected_airport],))
                        st.success("Airport deleted successfully")

def manage_terminals():
    st.title("Terminals Management")
    
    operation = st.selectbox("Operation", ["Create", "Read", "Update", "Delete"])
    
    if operation == "Create":
        with st.form("create_terminal"):
            # Get airports for dropdown
            airports = execute_query("SELECT airport_id, name FROM airports", fetch=True)
            if airports is not None and not airports.empty:
                airport_options = {row['name']: row['airport_id'] for _, row in airports.iterrows()}
                selected_airport = st.selectbox("Airport", options=list(airport_options.keys()))
                
                terminal_code = st.text_input("Terminal Code")
                
                if st.form_submit_button("Create"):
                    if not terminal_code:
                        st.error("Terminal code is required!")
                    else:
                        query = "INSERT INTO terminals (airport_id, terminal_code) VALUES (%s, %s) RETURNING terminal_id"
                        result = execute_query(query, (airport_options[selected_airport], terminal_code), fetch=True)
                        if result is not None:
                            st.success(f"Terminal created with ID: {result.iloc[0][0]}")
    
    elif operation == "Read":
        query = """
        SELECT t.terminal_id, a.name as airport_name, t.terminal_code 
        FROM terminals t
        JOIN airports a ON t.airport_id = a.airport_id
        """
        df = execute_query(query, fetch=True)
        if df is not None:
            st.dataframe(df)


def manage_gates():
    pass

def manage_flight_statuses():
    pass

def manage_payment_methods():
    pass

def manage_booking_statuses():
    pass

def manage_passengers():
    pass

def manage_flights():
    pass

def manage_flight_schedules():
    pass

def manage_bookings():
    pass

def manage_payments():
    pass

def manage_admin_roles():
    pass

def manage_admins():
    pass

def manage_notifications():
    pass

# Main app routing
if conn is not None:  # Only proceed if connection is established
    if page == "Airports":
        manage_airports()
    elif page == "Terminals":
        manage_terminals()
    elif page == "Gates":
        manage_gates()
    elif page == "Flight Statuses":
        manage_flight_statuses()
    elif page == "Payment Methods":
        manage_payment_methods()
    elif page == "Booking Statuses":
        manage_booking_statuses()
    elif page == "Passengers":
        manage_passengers()
    elif page == "Flights":
        manage_flights()
    elif page == "Flight Schedules":
        manage_flight_schedules()
    elif page == "Bookings":
        manage_bookings()
    elif page == "Payments":
        manage_payments()
    elif page == "Admin Roles":
        manage_admin_roles()
    elif page == "Admins":
        manage_admins()
    elif page == "Notifications":
        manage_notifications()

    # Close connection when done
    conn.close()
else:
    st.error("Failed to connect to database. Please check your connection settings.")
import streamlit as st
import psycopg2
from db_config import get_db_connection

# -----------------------------------
# CRUD functions for flights table
# -----------------------------------

def fetch_flights():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.flight_id, f.flight_number, a1.name AS origin_airport, a2.name AS destination_airport,
               f.aircraft_type, fs.status_name
        FROM flights f
        LEFT JOIN airports a1 ON f.origin_airport_id = a1.airport_id
        LEFT JOIN airports a2 ON f.destination_airport_id = a2.airport_id
        LEFT JOIN flight_statuses fs ON f.status_id = fs.status_id
        ORDER BY f.flight_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_airports():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT airport_id, name FROM airports ORDER BY name")
    airports = cur.fetchall()
    conn.close()
    return airports

def fetch_flight_statuses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT status_id, status_name FROM flight_statuses ORDER BY status_name")
    statuses = cur.fetchall()
    conn.close()
    return statuses

def add_flight(flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO flights (flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id))
        conn.commit()
        st.success("✅ Flight added successfully.")
    except psycopg2.Error as e:
        st.error(f"Error adding flight: {e.pgerror}")
    finally:
        conn.close()

def update_flight(flight_id, flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE flights
            SET flight_number = %s,
                origin_airport_id = %s,
                destination_airport_id = %s,
                aircraft_type = %s,
                status_id = %s
            WHERE flight_id = %s
        """, (flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id, flight_id))
        conn.commit()
        st.success("✏️ Flight updated successfully.")
    except psycopg2.Error as e:
        st.error(f"Error updating flight: {e.pgerror}")
    finally:
        conn.close()

def delete_flight(flight_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM flights WHERE flight_id = %s", (flight_id,))
        conn.commit()
        st.success("🗑️ Flight deleted.")
    except psycopg2.Error as e:
        st.error(f"Error deleting flight: {e.pgerror}")
    finally:
        conn.close()

# -----------------------------------
# Streamlit UI for flights management
# -----------------------------------

def show_flights_dashboard():
    st.title("✈️ Flight Management")

    # Show all flights
    st.subheader("📋 Existing Flights")
    flights = fetch_flights()
    if flights:
        st.table(flights)
    else:
        st.info("No flights found.")

    st.divider()

    # Prepare dropdowns
    airports = fetch_airports()
    airport_dict = {name: aid for aid, name in airports}

    statuses = fetch_flight_statuses()
    status_dict = {name: sid for sid, name in statuses}

    # Add flight
    st.subheader("➕ Add Flight")
    flight_number = st.text_input("Flight Number")
    origin_airport = st.selectbox("Origin Airport", list(airport_dict.keys()))
    destination_airport = st.selectbox("Destination Airport", list(airport_dict.keys()))
    aircraft_type = st.text_input("Aircraft Type")
    flight_status = st.selectbox("Flight Status", list(status_dict.keys()))

    if st.button("Add Flight"):
        if flight_number and origin_airport and destination_airport and aircraft_type:
            if origin_airport == destination_airport:
                st.warning("Origin and destination airports cannot be the same.")
            else:
                add_flight(
                    flight_number,
                    airport_dict[origin_airport],
                    airport_dict[destination_airport],
                    aircraft_type,
                    status_dict[flight_status]
                )
        else:
            st.warning("Please fill all the fields.")

    st.divider()

    # Update flight
    st.subheader("✏️ Update Flight")
    flight_id = st.text_input("Flight ID to Update")
    if flight_id:
        flight_number_upd = st.text_input("New Flight Number", key="upd_flight_number")
        origin_airport_upd = st.selectbox("New Origin Airport", list(airport_dict.keys()), key="upd_origin_airport")
        destination_airport_upd = st.selectbox("New Destination Airport", list(airport_dict.keys()), key="upd_dest_airport")
        aircraft_type_upd = st.text_input("New Aircraft Type", key="upd_aircraft_type")
        flight_status_upd = st.selectbox("New Flight Status", list(status_dict.keys()), key="upd_status")

        if st.button("Update Flight"):
            if flight_number_upd and origin_airport_upd and destination_airport_upd and aircraft_type_upd:
                if origin_airport_upd == destination_airport_upd:
                    st.warning("Origin and destination airports cannot be the same.")
                else:
                    update_flight(
                        flight_id,
                        flight_number_upd,
                        airport_dict[origin_airport_upd],
                        airport_dict[destination_airport_upd],
                        aircraft_type_upd,
                        status_dict[flight_status_upd]
                    )
            else:
                st.warning("Please fill all update fields.")

    st.divider()

    # Delete flight
    st.subheader("❌ Delete Flight")
    delete_id = st.text_input("Flight ID to Delete", key="delete_flight_id")
    if st.button("Delete Flight"):
        if delete_id:
            delete_flight(delete_id)
        else:
            st.warning("Please provide a Flight ID to delete.")

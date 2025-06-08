# modules/pilot_dashboard.py

import streamlit as st
from config.db_config import get_cursor, get_connection

def fetch_flights_by_pilot(pilot_id):
    cursor = get_cursor()
    # You might have a table like pilot_assignments (not in schema)
    # For now, we assume pilot sees all flights for demo
    cursor.execute("""
        SELECT f.flight_id, f.flight_number, 
               a1.name AS origin, a2.name AS destination, 
               s.departure_time, s.arrival_time, fs.status_name
        FROM flights f
        JOIN airports a1 ON f.origin_airport_id = a1.airport_id
        JOIN airports a2 ON f.destination_airport_id = a2.airport_id
        JOIN flight_schedules s ON f.flight_id = s.flight_id
        JOIN flight_statuses fs ON f.status_id = fs.status_id
        ORDER BY s.departure_time
    """)
    return cursor.fetchall()

def fetch_statuses():
    cursor = get_cursor()
    cursor.execute("SELECT status_id, status_name FROM flight_statuses")
    return cursor.fetchall()

def update_flight_status(flight_id, status_id):
    cursor = get_cursor()
    conn = get_connection()
    cursor.execute("UPDATE flights SET status_id = %s WHERE flight_id = %s", (status_id, flight_id))
    conn.commit()

def pilot_dashboard(pilot):
    st.subheader("Pilot Flight Dashboard")

    st.markdown(f"**Welcome, Captain {pilot['full_name']}!**")

    flights = fetch_flights_by_pilot(pilot['admin_id'])
    if not flights:
        st.info("No assigned flights at the moment.")
        return

    st.write("### Assigned Flights")
    selected_flight_str = st.selectbox(
        "Select Flight",
        [f"{f['flight_number']} | {f['origin']} ➜ {f['destination']} | {f['departure_time']}" for f in flights]
    )

    selected_flight_id = next(
        f['flight_id'] for f in flights 
        if f"{f['flight_number']} | {f['origin']} ➜ {f['destination']} | {f['departure_time']}" == selected_flight_str
    )

    selected_flight = next(f for f in flights if f['flight_id'] == selected_flight_id)

    st.write("### Flight Details")
    st.write(f"**Flight Number**: {selected_flight['flight_number']}")
    st.write(f"**From**: {selected_flight['origin']}  ➜  **To**: {selected_flight['destination']}")
    st.write(f"**Departure**: {selected_flight['departure_time']}")
    st.write(f"**Arrival**: {selected_flight['arrival_time']}")
    st.write(f"**Current Status**: {selected_flight['status_name']}")

    st.write("### Update Flight Status")
    statuses = fetch_statuses()
    status_dict = {s['status_name']: s['status_id'] for s in statuses}

    selected_status = st.selectbox("Change Status", list(status_dict.keys()), index=list(status_dict.keys()).index(selected_flight['status_name']))
    if st.button("Update Status"):
        update_flight_status(selected_flight_id, status_dict[selected_status])
        st.success("Flight status updated.")
        st.experimental_rerun()

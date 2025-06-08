import streamlit as st
import psycopg2
from config.db_config import get_db_connection

# -----------------------------------
# CRUD Functions for Bookings
# -----------------------------------

def fetch_bookings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.booking_id, p.full_name, fs.schedule_id, b.seat_number, bs.status_name, b.booked_at
        FROM bookings b
        JOIN passengers p ON b.passenger_id = p.passenger_id
        JOIN flight_schedules fs ON b.schedule_id = fs.schedule_id
        JOIN booking_statuses bs ON b.status_id = bs.status_id
        ORDER BY b.booking_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_passengers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT passenger_id, full_name FROM passengers ORDER BY full_name")
    passengers = cur.fetchall()
    conn.close()
    return passengers

def fetch_schedules():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT schedule_id, flight_id, departure_time, arrival_time
        FROM flight_schedules
        ORDER BY schedule_id
    """)
    schedules = cur.fetchall()
    conn.close()
    return schedules

def fetch_booking_statuses():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT status_id, status_name FROM booking_statuses ORDER BY status_id")
    statuses = cur.fetchall()
    conn.close()
    return statuses

def add_booking(passenger_id, schedule_id, seat_number, status_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO bookings (passenger_id, schedule_id, seat_number, status_id)
            VALUES (%s, %s, %s, %s)
        """, (passenger_id, schedule_id, seat_number, status_id))
        conn.commit()
        st.success("✅ Booking added successfully.")
    except psycopg2.Error as e:
        st.error(f"Error adding booking: {e.pgerror}")
    finally:
        conn.close()

def update_booking(booking_id, passenger_id, schedule_id, seat_number, status_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE bookings
            SET passenger_id = %s, schedule_id = %s, seat_number = %s, status_id = %s
            WHERE booking_id = %s
        """, (passenger_id, schedule_id, seat_number, status_id, booking_id))
        conn.commit()
        st.success("✏️ Booking updated successfully.")
    except psycopg2.Error as e:
        st.error(f"Error updating booking: {e.pgerror}")
    finally:
        conn.close()

def delete_booking(booking_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM bookings WHERE booking_id = %s", (booking_id,))
        conn.commit()
        st.success("🗑️ Booking deleted.")
    except psycopg2.Error as e:
        st.error(f"Error deleting booking: {e.pgerror}")
    finally:
        conn.close()

# -----------------------------------
# Streamlit UI
# -----------------------------------

def show_bookings_dashboard():
    st.title("🛎️ Booking Management")

    # Display Bookings
    st.subheader("📋 Existing Bookings")
    bookings = fetch_bookings()
    if bookings:
        st.table(bookings)
    else:
        st.info("No bookings found.")

    st.divider()

    # Prepare dropdown options
    passengers = fetch_passengers()
    passenger_dict = {name: pid for pid, name in passengers}
    schedules = fetch_schedules()
    schedule_dict = {
        f"ID {sid} | Flight {fid} | Dep: {dep} | Arr: {arr}": sid 
        for sid, fid, dep, arr in schedules
    }
    statuses = fetch_booking_statuses()
    status_dict = {name: sid for sid, name in statuses}

    # Add Booking
    st.subheader("➕ Add Booking")
    selected_passenger = st.selectbox("Passenger", list(passenger_dict.keys()))
    selected_schedule = st.selectbox("Flight Schedule", list(schedule_dict.keys()))
    seat_number = st.text_input("Seat Number")
    selected_status = st.selectbox("Booking Status", list(status_dict.keys()))

    if st.button("Add Booking"):
        if seat_number and selected_passenger and selected_schedule:
            add_booking(
                passenger_dict[selected_passenger],
                schedule_dict[selected_schedule],
                seat_number,
                status_dict[selected_status]
            )
        else:
            st.warning("Please fill all required fields.")

    st.divider()

    # Update Booking
    st.subheader("✏️ Update Booking")
    booking_id = st.text_input("Booking ID to Update")
    if booking_id:
        selected_passenger_upd = st.selectbox("New Passenger", list(passenger_dict.keys()), key="upd_passenger")
        selected_schedule_upd = st.selectbox("New Flight Schedule", list(schedule_dict.keys()), key="upd_schedule")
        seat_number_upd = st.text_input("New Seat Number", key="upd_seat")
        selected_status_upd = st.selectbox("New Booking Status", list(status_dict.keys()), key="upd_status")

        if st.button("Update Booking"):
            if booking_id and seat_number_upd:
                update_booking(
                    booking_id,
                    passenger_dict[selected_passenger_upd],
                    schedule_dict[selected_schedule_upd],
                    seat_number_upd,
                    status_dict[selected_status_upd]
                )
            else:
                st.warning("Please fill all update fields.")

    st.divider()

    # Delete Booking
    st.subheader("❌ Delete Booking")
    delete_id = st.text_input("Booking ID to Delete", key="delete_booking_id")
    if st.button("Delete Booking"):
        if delete_id:
            delete_booking(delete_id)
        else:
            st.warning("Please provide a Booking ID to delete.")

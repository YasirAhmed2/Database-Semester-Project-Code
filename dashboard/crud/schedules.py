import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for flight_schedules table
# ------------------------------

def fetch_schedules():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT fs.schedule_id, f.flight_number, fs.departure_time, fs.arrival_time, g.gate_code
        FROM flight_schedules fs
        JOIN flights f ON fs.flight_id = f.flight_id
        JOIN gates g ON fs.gate_id = g.gate_id
        ORDER BY fs.departure_time DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_flights():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT flight_id, flight_number FROM flights ORDER BY flight_number")
    flights = cur.fetchall()
    conn.close()
    return flights

def fetch_gates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT g.gate_id, t.terminal_code, g.gate_code, a.code AS airport_code
        FROM gates g
        JOIN terminals t ON g.terminal_id = t.terminal_id
        JOIN airports a ON t.airport_id = a.airport_id
        ORDER BY a.code, t.terminal_code, g.gate_code
    """)
    gates = cur.fetchall()
    conn.close()
    return gates

def add_schedule(flight_id, departure_time, arrival_time, gate_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO flight_schedules (flight_id, departure_time, arrival_time, gate_id)
            VALUES (%s, %s, %s, %s)
        """, (flight_id, departure_time, arrival_time, gate_id))
        conn.commit()
        st.success("✅ Flight schedule added successfully.")
    except Exception as e:
        st.error(f"Error adding flight schedule: {e}")
    finally:
        conn.close()

def update_schedule(schedule_id, flight_id, departure_time, arrival_time, gate_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE flight_schedules
            SET flight_id = %s,
                departure_time = %s,
                arrival_time = %s,
                gate_id = %s
            WHERE schedule_id = %s
        """, (flight_id, departure_time, arrival_time, gate_id, schedule_id))
        conn.commit()
        st.success("✏️ Flight schedule updated successfully.")
    except Exception as e:
        st.error(f"Error updating flight schedule: {e}")
    finally:
        conn.close()

def delete_schedule(schedule_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM flight_schedules WHERE schedule_id = %s", (schedule_id,))
        conn.commit()
        st.success("🗑️ Flight schedule deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting flight schedule: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for flight schedules
# ------------------------------

def show_flight_schedules_dashboard():
    st.title("🛫 Flight Schedules Management")

    # Display existing schedules
    st.subheader("📋 Existing Flight Schedules")
    schedules = fetch_schedules()
    if schedules:
        st.table(schedules)
    else:
        st.info("No flight schedules found.")

    st.divider()

    # Prepare dropdown data
    flights = fetch_flights()
    flight_dict = {f[1]: f[0] for f in flights}
    gates = fetch_gates()
    # Format gate display as "AirportCode - TerminalCode - GateCode"
    gate_dict = {f"{g[3]} - {g[1]} - {g[2]}": g[0] for g in gates}

    # Add new schedule
    st.subheader("➕ Add Flight Schedule")
    flight_number = st.selectbox("Flight Number", list(flight_dict.keys()))
    departure_time = st.date_input("Departure Date")
    dep_time_h = st.number_input("Departure Hour (0-23)", 0, 23, 12)
    dep_time_m = st.number_input("Departure Minute (0-59)", 0, 59, 0)

    arrival_time = st.date_input("Arrival Date")
    arr_time_h = st.number_input("Arrival Hour (0-23)", 0, 23, 15)
    arr_time_m = st.number_input("Arrival Minute (0-59)", 0, 59, 0)

    gate_display = st.selectbox("Gate", list(gate_dict.keys()))

    from datetime import datetime

    dep_datetime = datetime.combine(departure_time, datetime.min.time()).replace(hour=dep_time_h, minute=dep_time_m)
    arr_datetime = datetime.combine(arrival_time, datetime.min.time()).replace(hour=arr_time_h, minute=arr_time_m)

    if st.button("Add Schedule"):
        if dep_datetime < arr_datetime:
            add_schedule(flight_dict[flight_number], dep_datetime, arr_datetime, gate_dict[gate_display])
        else:
            st.warning("Arrival time must be after departure time.")

    st.divider()

    # Update existing schedule
    st.subheader("✏️ Update Flight Schedule")
    schedule_ids = [str(s[0]) for s in schedules]
    selected_schedule_id = st.selectbox("Select Schedule ID", options=schedule_ids, key="upd_schedule")

    if selected_schedule_id:
        # Fetch current schedule data for pre-filling (optional enhancement)
        schedule_to_edit = next((s for s in schedules if str(s[0]) == selected_schedule_id), None)
        if schedule_to_edit:
            cur_flight_num = schedule_to_edit[1]
            cur_dep_time = schedule_to_edit[2]
            cur_arr_time = schedule_to_edit[3]
            cur_gate = schedule_to_edit[4]

            upd_flight_num = st.selectbox("Flight Number", list(flight_dict.keys()), index=list(flight_dict.keys()).index(cur_flight_num), key="upd_flight_num")
            
            # Dates and times for update
            from datetime import datetime as dt

            upd_dep_date = st.date_input("Departure Date", value=cur_dep_time.date(), key="upd_dep_date")
            upd_dep_hour = st.number_input("Departure Hour (0-23)", 0, 23, value=cur_dep_time.hour, key="upd_dep_hour")
            upd_dep_minute = st.number_input("Departure Minute (0-59)", 0, 59, value=cur_dep_time.minute, key="upd_dep_minute")

            upd_arr_date = st.date_input("Arrival Date", value=cur_arr_time.date(), key="upd_arr_date")
            upd_arr_hour = st.number_input("Arrival Hour (0-23)", 0, 23, value=cur_arr_time.hour, key="upd_arr_hour")
            upd_arr_minute = st.number_input("Arrival Minute (0-59)", 0, 59, value=cur_arr_time.minute, key="upd_arr_minute")

            upd_gate = st.selectbox("Gate", list(gate_dict.keys()), index=list(gate_dict.keys()).index(cur_gate), key="upd_gate")

            upd_dep_datetime = dt.combine(upd_dep_date, dt.min.time()).replace(hour=upd_dep_hour, minute=upd_dep_minute)
            upd_arr_datetime = dt.combine(upd_arr_date, dt.min.time()).replace(hour=upd_arr_hour, minute=upd_arr_minute)

            if st.button("Update Schedule"):
                if upd_dep_datetime < upd_arr_datetime:
                    update_schedule(
                        selected_schedule_id,
                        flight_dict[upd_flight_num],
                        upd_dep_datetime,
                        upd_arr_datetime,
                        gate_dict[upd_gate]
                    )
                else:
                    st.warning("Arrival time must be after departure time.")

    st.divider()

    # Delete schedule
    st.subheader("❌ Delete Flight Schedule")
    delete_id = st.text_input("Schedule ID to Delete", key="delete_schedule_id")
    if st.button("Delete Schedule"):
        if delete_id:
            delete_schedule(delete_id)
        else:
            st.warning("Please enter a Schedule ID to delete.")

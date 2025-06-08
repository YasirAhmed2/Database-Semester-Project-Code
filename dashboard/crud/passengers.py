import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for passengers table
# ------------------------------

def fetch_passengers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT passenger_id, full_name, email, phone_number, passport_number, nationality, created_at
        FROM passengers
        ORDER BY created_at DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_passenger(full_name, email, phone_number, passport_number, nationality):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO passengers (full_name, email, phone_number, passport_number, nationality)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, phone_number, passport_number, nationality))
        conn.commit()
        st.success("✅ Passenger added successfully.")
    except Exception as e:
        st.error(f"Error adding passenger: {e}")
    finally:
        conn.close()

def update_passenger(passenger_id, full_name, email, phone_number, passport_number, nationality):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE passengers
            SET full_name = %s,
                email = %s,
                phone_number = %s,
                passport_number = %s,
                nationality = %s
            WHERE passenger_id = %s
        """, (full_name, email, phone_number, passport_number, nationality, passenger_id))
        conn.commit()
        st.success("✏️ Passenger updated successfully.")
    except Exception as e:
        st.error(f"Error updating passenger: {e}")
    finally:
        conn.close()

def delete_passenger(passenger_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM passengers WHERE passenger_id = %s", (passenger_id,))
        conn.commit()
        st.success("🗑️ Passenger deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting passenger: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for passengers
# ------------------------------

def show_passengers_dashboard():
    st.title("🧳 Passengers Management")

    # List passengers
    st.subheader("📋 Existing Passengers")
    passengers = fetch_passengers()
    if passengers:
        st.table(passengers)
    else:
        st.info("No passengers found.")

    st.divider()

    # Add passenger form
    st.subheader("➕ Add Passenger")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone_number = st.text_input("Phone Number")
    passport_number = st.text_input("Passport Number")
    nationality = st.text_input("Nationality")

    if st.button("Add Passenger"):
        if full_name and email and passport_number:
            add_passenger(full_name, email, phone_number, passport_number, nationality)
        else:
            st.warning("Please fill at least Full Name, Email, and Passport Number.")

    st.divider()

    # Update passenger form
    st.subheader("✏️ Update Passenger")
    passenger_id = st.text_input("Passenger ID to Update")
    if passenger_id:
        full_name_upd = st.text_input("Full Name", key="upd_full_name")
        email_upd = st.text_input("Email", key="upd_email")
        phone_number_upd = st.text_input("Phone Number", key="upd_phone")
        passport_number_upd = st.text_input("Passport Number", key="upd_passport")
        nationality_upd = st.text_input("Nationality", key="upd_nationality")

        if st.button("Update Passenger"):
            if full_name_upd and email_upd and passport_number_upd:
                update_passenger(passenger_id, full_name_upd, email_upd, phone_number_upd, passport_number_upd, nationality_upd)
            else:
                st.warning("Please fill at least Full Name, Email, and Passport Number.")

    st.divider()

    # Delete passenger form
    st.subheader("❌ Delete Passenger")
    delete_id = st.text_input("Passenger ID to Delete", key="delete_passenger_id")
    if st.button("Delete Passenger"):
        if delete_id:
            delete_passenger(delete_id)
        else:
            st.warning("Please enter a Passenger ID to delete.")

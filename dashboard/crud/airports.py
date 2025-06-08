import streamlit as st
import psycopg2
from config.db_config import get_db_connection

# -------------------------------------
# CRUD Functions for Airports
# -------------------------------------

def fetch_airports():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM airports ORDER BY airport_id")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_airport(name, city, country, code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO airports (name, city, country, code)
            VALUES (%s, %s, %s, %s)
        """, (name, city, country, code))
        conn.commit()
        st.success("✅ Airport added successfully.")
    except psycopg2.Error as e:
        st.error(f"Error adding airport: {e.pgerror}")
    finally:
        conn.close()

def update_airport(airport_id, name, city, country, code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE airports
            SET name = %s, city = %s, country = %s, code = %s
            WHERE airport_id = %s
        """, (name, city, country, code, airport_id))
        conn.commit()
        st.success("✏️ Airport updated successfully.")
    except psycopg2.Error as e:
        st.error(f"Error updating airport: {e.pgerror}")
    finally:
        conn.close()

def delete_airport(airport_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM airports WHERE airport_id = %s", (airport_id,))
        conn.commit()
        st.success("🗑️ Airport deleted.")
    except psycopg2.Error as e:
        st.error(f"Error deleting airport: {e.pgerror}")
    finally:
        conn.close()

# -------------------------------------
# Streamlit UI
# -------------------------------------

def show_airports_dashboard():
    st.title("🛫 Airport Management")

    # Display Existing Airports
    st.subheader("📋 Existing Airports")
    airports = fetch_airports()
    if airports:
        st.table(airports)
    else:
        st.info("No airports found.")

    st.divider()

    # Add Airport
    st.subheader("➕ Add Airport")
    name = st.text_input("Name")
    city = st.text_input("City")
    country = st.text_input("Country")
    code = st.text_input("Airport Code (e.g., LAX, JFK)")

    if st.button("Add Airport"):
        if name and code:
            add_airport(name, city, country, code)
        else:
            st.warning("Airport Name and Code are required.")

    st.divider()

    # Update Airport
    st.subheader("✏️ Update Airport")
    update_id = st.text_input("Airport ID to Update")
    update_name = st.text_input("New Name")
    update_city = st.text_input("New City")
    update_country = st.text_input("New Country")
    update_code = st.text_input("New Code")

    if st.button("Update Airport"):
        if update_id and update_name and update_code:
            update_airport(update_id, update_name, update_city, update_country, update_code)
        else:
            st.warning("Airport ID, Name, and Code are required to update.")

    st.divider()

    # Delete Airport
    st.subheader("❌ Delete Airport")
    delete_id = st.text_input("Airport ID to Delete")
    if st.button("Delete Airport"):
        if delete_id:
            delete_airport(delete_id)
        else:
            st.warning("Provide an Airport ID to delete.")

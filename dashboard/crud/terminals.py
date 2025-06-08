import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for terminals table
# ------------------------------

def fetch_terminals():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.terminal_id, a.name AS airport_name, t.terminal_code
        FROM terminals t
        JOIN airports a ON t.airport_id = a.airport_id
        ORDER BY a.name, t.terminal_code
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

def add_terminal(airport_id, terminal_code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO terminals (airport_id, terminal_code)
            VALUES (%s, %s)
        """, (airport_id, terminal_code))
        conn.commit()
        st.success("✅ Terminal added successfully.")
    except Exception as e:
        st.error(f"Error adding terminal: {e}")
    finally:
        conn.close()

def update_terminal(terminal_id, airport_id, terminal_code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE terminals
            SET airport_id = %s, terminal_code = %s
            WHERE terminal_id = %s
        """, (airport_id, terminal_code, terminal_id))
        conn.commit()
        st.success("✏️ Terminal updated successfully.")
    except Exception as e:
        st.error(f"Error updating terminal: {e}")
    finally:
        conn.close()

def delete_terminal(terminal_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM terminals WHERE terminal_id = %s", (terminal_id,))
        conn.commit()
        st.success("🗑️ Terminal deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting terminal: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for terminals management
# ------------------------------

def show_terminals_dashboard():
    st.title("🏢 Terminal Management")

    # Display existing terminals
    st.subheader("📋 Existing Terminals")
    terminals = fetch_terminals()
    if terminals:
        st.table(terminals)
    else:
        st.info("No terminals found.")

    st.divider()

    # Prepare dropdown data
    airports = fetch_airports()
    airport_dict = {a[1]: a[0] for a in airports}

    # Add new terminal
    st.subheader("➕ Add Terminal")
    airport_name = st.selectbox("Select Airport", list(airport_dict.keys()))
    terminal_code = st.text_input("Terminal Code")

    if st.button("Add Terminal"):
        if terminal_code.strip() == "":
            st.warning("Terminal code cannot be empty.")
        else:
            add_terminal(airport_dict[airport_name], terminal_code.strip())

    st.divider()

    # Update existing terminal
    st.subheader("✏️ Update Terminal")
    terminal_ids = [str(t[0]) for t in terminals]
    selected_terminal_id = st.selectbox("Select Terminal ID", options=terminal_ids, key="upd_terminal")

    if selected_terminal_id:
        terminal_to_edit = next((t for t in terminals if str(t[0]) == selected_terminal_id), None)
        if terminal_to_edit:
            cur_airport_name = terminal_to_edit[1]
            cur_terminal_code = terminal_to_edit[2]

            upd_airport_name = st.selectbox("Airport", list(airport_dict.keys()), index=list(airport_dict.keys()).index(cur_airport_name), key="upd_airport")
            upd_terminal_code = st.text_input("Terminal Code", value=cur_terminal_code, key="upd_terminal_code")

            if st.button("Update Terminal"):
                if upd_terminal_code.strip() == "":
                    st.warning("Terminal code cannot be empty.")
                else:
                    update_terminal(int(selected_terminal_id), airport_dict[upd_airport_name], upd_terminal_code.strip())

    st.divider()

    # Delete terminal
    st.subheader("❌ Delete Terminal")
    delete_id = st.text_input("Terminal ID to Delete", key="delete_terminal_id")
    if st.button("Delete Terminal"):
        if delete_id:
            delete_terminal(delete_id)
        else:
            st.warning("Please enter a Terminal ID to delete.")

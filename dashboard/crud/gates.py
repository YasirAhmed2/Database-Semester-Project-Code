import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for gates table
# ------------------------------

def fetch_gates():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT g.gate_id, t.terminal_code, a.name AS airport_name, g.gate_code
        FROM gates g
        JOIN terminals t ON g.terminal_id = t.terminal_id
        JOIN airports a ON t.airport_id = a.airport_id
        ORDER BY g.gate_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_terminals():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.terminal_id, t.terminal_code, a.name AS airport_name
        FROM terminals t
        JOIN airports a ON t.airport_id = a.airport_id
        ORDER BY a.name, t.terminal_code
    """)
    terminals = cur.fetchall()
    conn.close()
    return terminals

def add_gate(terminal_id, gate_code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO gates (terminal_id, gate_code) VALUES (%s, %s)", (terminal_id, gate_code))
        conn.commit()
        st.success("✅ Gate added successfully.")
    except Exception as e:
        st.error(f"Error adding gate: {e}")
    finally:
        conn.close()

def update_gate(gate_id, terminal_id, gate_code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE gates
            SET terminal_id = %s, gate_code = %s
            WHERE gate_id = %s
        """, (terminal_id, gate_code, gate_id))
        conn.commit()
        st.success("✏️ Gate updated successfully.")
    except Exception as e:
        st.error(f"Error updating gate: {e}")
    finally:
        conn.close()

def delete_gate(gate_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM gates WHERE gate_id = %s", (gate_id,))
        conn.commit()
        st.success("🗑️ Gate deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting gate: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for gates
# ------------------------------

def show_gates_dashboard():
    st.title("🛂 Gates Management")

    # List all gates
    st.subheader("📋 Existing Gates")
    gates = fetch_gates()
    if gates:
        st.table(gates)
    else:
        st.info("No gates found.")

    st.divider()

    # Prepare dropdown for terminals
    terminals = fetch_terminals()
    terminal_display = [f"{t[2]} - Terminal {t[1]}" for t in terminals]
    terminal_dict = {f"{t[2]} - Terminal {t[1]}": t[0] for t in terminals}

    # Add gate
    st.subheader("➕ Add Gate")
    terminal_sel = st.selectbox("Select Terminal", terminal_display)
    gate_code = st.text_input("Gate Code")

    if st.button("Add Gate"):
        if gate_code:
            add_gate(terminal_dict[terminal_sel], gate_code)
        else:
            st.warning("Please enter a gate code.")

    st.divider()

    # Update gate
    st.subheader("✏️ Update Gate")
    gate_id = st.text_input("Gate ID to Update")
    if gate_id:
        terminal_upd = st.selectbox("New Terminal", terminal_display, key="upd_terminal")
        gate_code_upd = st.text_input("New Gate Code", key="upd_gate_code")

        if st.button("Update Gate"):
            if gate_code_upd:
                update_gate(gate_id, terminal_dict[terminal_upd], gate_code_upd)
            else:
                st.warning("Please enter a new gate code.")

    st.divider()

    # Delete gate
    st.subheader("❌ Delete Gate")
    delete_id = st.text_input("Gate ID to Delete", key="delete_gate_id")
    if st.button("Delete Gate"):
        if delete_id:
            delete_gate(delete_id)
        else:
            st.warning("Please enter a Gate ID to delete.")

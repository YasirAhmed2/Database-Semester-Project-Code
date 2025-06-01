# app.py
import streamlit as st
import pandas as pd
from db import SessionLocal
from login import login_user
from utils import export_to_excel, filter_dataframe
from audit_logs import log_action
from sqlalchemy import text
import re

# Setup
session = SessionLocal()
st.set_page_config(layout="wide")
st.title("🛫 Airport Flight Management")

# Session state
if "user" not in st.session_state:
    st.session_state.user = None

# Caching: load data
@st.cache_data(ttl=60)
def load_table_data(table):
    return pd.read_sql(f"SELECT * FROM {table}", session.bind)

# Get primary key of a table
def get_primary_key_column(session, table_name):
    if not re.match(r'^\w+$', table_name):
        raise ValueError("Invalid table name")
    query = f"""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = '{table_name}'::regclass AND i.indisprimary;
    """
    result = session.execute(text(query)).fetchone()
    return result[0] if result else None

# Login form
def login():
    with st.form("login_form"):
        st.subheader("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = login_user(session, email, password)
            if user:
                st.session_state.user = dict(user._mapping)
                st.success(f"Welcome, {user.full_name}")
                st.rerun()
            else:
                st.error("Invalid login")

# Dashboard
def dashboard():
    st.sidebar.title("📋 Dashboard Menu")
    tables = [
        "airports", "terminals", "gates", "passengers", "flights", "flight_schedules",
        "bookings", "payments", "admins"
    ]
    table = st.sidebar.selectbox("Select Table", tables)

    # Load and filter table
    df = load_table_data(table)
    search = st.text_input("🔍 Search Table")
    if search:
        df = filter_dataframe(df, search)
    st.dataframe(df, use_container_width=True)

    # Export
    if st.download_button("📤 Export to Excel", data=export_to_excel(df),
                          file_name=f"{table}.xlsx", mime="application/vnd.ms-excel"):
        st.success("Downloaded")

    # ➕ Insert Record
    st.subheader(f"➕ Add New Record to {table}")
    columns = pd.read_sql(f"SELECT * FROM {table} LIMIT 1", session.bind).columns.tolist()
    with st.form("insert_form"):
        new_data = {col: st.text_input(f"{col}") for col in columns if col != 'id'}
        submit_insert = st.form_submit_button("Insert")
        if submit_insert:
            try:
                col_str = ", ".join(new_data.keys())
                val_str = ", ".join([f":{col}" for col in new_data])
                insert_query = text(f"INSERT INTO {table} ({col_str}) VALUES ({val_str}) RETURNING *")
                result = session.execute(insert_query, new_data)
                session.commit()
                inserted_id = result.fetchone()[0]
                log_action(session, table, "INSERT", inserted_id, st.session_state.user['admin_id'])
                st.success("✅ Inserted Successfully!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to insert: {e}")

    # ❌ Delete Record
    st.subheader("❌ Delete Record")
    pk_column = get_primary_key_column(session, table)
    with st.form("delete_form"):
        del_id = st.text_input(f"Enter {pk_column} to delete")
        submit_delete = st.form_submit_button("Delete")
        if submit_delete:
            try:
                delete_query = text(f"DELETE FROM {table} WHERE {pk_column} = :id")
                session.execute(delete_query, {"id": del_id})
                session.commit()
                log_action(session, table, "DELETE", del_id, st.session_state.user['admin_id'])
                st.success("✅ Deleted Successfully!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to delete: {e}")

    # ✏️ Update Record
    st.subheader("✏️ Update Record")
    if not pk_column:
        st.error(f"❌ No primary key found for table `{table}`.")
        return

    with st.form("update_form"):
        update_id = st.text_input(f"Enter {pk_column} to update")
        submit_lookup = st.form_submit_button("Load Record")

    if update_id and submit_lookup:
        record = session.execute(
            text(f"SELECT * FROM {table} WHERE {pk_column} = :pk"),
            {"pk": update_id}
        ).fetchone()
        if record:
            record_dict = dict(record._mapping)
            with st.form("actual_update_form"):
                updated_data = {}
                for key, value in record_dict.items():
                    if key == pk_column:
                        st.text_input(f"{key}", value, disabled=True)
                    else:
                        updated_data[key] = st.text_input(f"{key}", str(value))
                update_submit = st.form_submit_button("Update")
                if update_submit:
                    try:
                        update_query = text(f"""
                            UPDATE {table} SET
                            {', '.join([f"{col} = :{col}" for col in updated_data])}
                            WHERE {pk_column} = :pk
                        """)
                        updated_data["pk"] = update_id
                        session.execute(update_query, updated_data)
                        session.commit()
                        log_action(session, table, "UPDATE", update_id, st.session_state.user['admin_id'])
                        st.success("✅ Updated Successfully!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to update: {e}")
        else:
            st.warning(f"No record found with `{pk_column}` = {update_id}.")

# Run
if st.session_state.user:
    dashboard()
else:
    login()

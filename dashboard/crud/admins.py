import streamlit as st
import psycopg2
from config.db_config import get_db_connection
from auth.auth_utils import hash_password

# ----------------------------- #
# CRUD FUNCTIONS FOR ADMINS    #
# ----------------------------- #

def fetch_admins():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.admin_id, a.full_name, a.email, r.role_name
        FROM admins a
        JOIN admin_roles r ON a.role_id = r.role_id
        ORDER BY a.admin_id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_roles():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name FROM admin_roles")
    roles = cur.fetchall()
    conn.close()
    return roles

def add_admin(full_name, email, password, role_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        hashed_pw = hash_password(password)
        cur.execute("""
            INSERT INTO admins (full_name, email, password, role_id)
            VALUES (%s, %s, %s, %s)
        """, (full_name, email, hashed_pw, role_id))
        conn.commit()
        st.success("Admin added successfully.")
    except psycopg2.Error as e:
        st.error(f"Error: {e.pgerror}")
    finally:
        conn.close()

def update_admin(admin_id, full_name, email, role_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE admins
            SET full_name = %s, email = %s, role_id = %s
            WHERE admin_id = %s
        """, (full_name, email, role_id, admin_id))
        conn.commit()
        st.success("Admin updated successfully.")
    except psycopg2.Error as e:
        st.error(f"Error: {e.pgerror}")
    finally:
        conn.close()

def delete_admin(admin_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
        conn.commit()
        st.success("Admin deleted.")
    except psycopg2.Error as e:
        st.error(f"Error: {e.pgerror}")
    finally:
        conn.close()

# ----------------------------- #
# ADMIN DASHBOARD UI           #
# ----------------------------- #

def show_admin_dashboard():
    st.title("👤 Admin Management")

    st.subheader("All Admins")
    admins = fetch_admins()
    if admins:
        st.table(admins)
    else:
        st.info("No admins found.")

    st.divider()

    st.subheader("➕ Add New Admin")
    roles = fetch_roles()
    role_dict = {r['role_name']: r['role_id'] for r in roles}
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role_name = st.selectbox("Role", list(role_dict.keys()))

    if st.button("Add Admin"):
        if name and email and password:
            add_admin(name, email, password, role_dict[role_name])
        else:
            st.warning("All fields are required.")

    st.divider()

    st.subheader("✏️ Update Admin")
    admin_id = st.text_input("Admin ID to Update")
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_role = st.selectbox("New Role", list(role_dict.keys()), key="update_role")

    if st.button("Update Admin"):
        if admin_id and new_name and new_email:
            update_admin(admin_id, new_name, new_email, role_dict[new_role])
        else:
            st.warning("Please provide all update details.")

    st.divider()

    st.subheader("❌ Delete Admin")
    del_id = st.text_input("Admin ID to Delete")
    if st.button("Delete Admin"):
        if del_id:
            delete_admin(del_id)
        else:
            st.warning("Provide an ID to delete.")

# modules/admin_dashboard.py
import streamlit as st
from config.db_config import get_cursor, get_connection

def fetch_admins():
    cursor = get_cursor()
    cursor.execute("""
        SELECT a.admin_id, a.full_name, a.email, r.role_name 
        FROM admins a
        JOIN admin_roles r ON a.role_id = r.role_id
        ORDER BY a.admin_id
    """)
    return cursor.fetchall()

def fetch_roles():
    cursor = get_cursor()
    cursor.execute("SELECT role_id, role_name FROM admin_roles ORDER BY role_name")
    return cursor.fetchall()

def add_admin(full_name, email, password, role_id):
    cursor = get_cursor()
    conn = get_connection()
    cursor.execute("""
        INSERT INTO admins (full_name, email, password, role_id) 
        VALUES (%s, %s, %s, %s)
    """, (full_name, email, password, role_id))
    conn.commit()

def update_admin(admin_id, full_name, email, password, role_id):
    cursor = get_cursor()
    conn = get_connection()
    cursor.execute("""
        UPDATE admins 
        SET full_name = %s, email = %s, password = %s, role_id = %s
        WHERE admin_id = %s
    """, (full_name, email, password, role_id, admin_id))
    conn.commit()

def delete_admin(admin_id):
    cursor = get_cursor()
    conn = get_connection()
    cursor.execute("DELETE FROM admins WHERE admin_id = %s", (admin_id,))
    conn.commit()

def admin_dashboard():
    st.subheader("Admin Management Panel")

    st.write("### All Admin Users")
    admins = fetch_admins()
    st.dataframe(admins)

    st.write("### Add New Admin")
    with st.form("add_admin_form"):
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        roles = fetch_roles()
        role_dict = {r['role_name']: r['role_id'] for r in roles}
        selected_role = st.selectbox("Select Role", list(role_dict.keys()))
        submitted = st.form_submit_button("Add Admin")
        if submitted:
            add_admin(full_name, email, password, role_dict[selected_role])
            st.success("Admin added successfully.")
            st.experimental_rerun()

    st.write("### Update/Delete Admin")
    selected_admin = st.selectbox("Select Admin to Update/Delete", [f"{a['admin_id']} - {a['full_name']}" for a in admins])
    admin_id = int(selected_admin.split(" - ")[0])
    admin_data = next((a for a in admins if a['admin_id'] == admin_id), None)

    if admin_data:
        with st.form("update_admin_form"):
            full_name = st.text_input("Full Name", admin_data['full_name'])
            email = st.text_input("Email", admin_data['email'])
            password = st.text_input("Password", type="password")
            selected_role = st.selectbox("Select Role", list(role_dict.keys()), index=list(role_dict.keys()).index(admin_data['role_name']))
            update_btn = st.form_submit_button("Update Admin")
            if update_btn:
                update_admin(admin_id, full_name, email, password, role_dict[selected_role])
                st.success("Admin updated.")
                st.experimental_rerun()

        if st.button("Delete Admin"):
            delete_admin(admin_id)
            st.warning("Admin deleted.")
            st.experimental_rerun()

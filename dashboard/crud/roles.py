import streamlit as st
from config.db_config import get_db_connection

# ------------------------------
# CRUD functions for admin_roles table
# ------------------------------

def fetch_roles():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name FROM admin_roles ORDER BY role_name")
    roles = cur.fetchall()
    conn.close()
    return roles

def add_role(role_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO admin_roles (role_name) VALUES (%s)", (role_name,))
        conn.commit()
        st.success(f"✅ Role '{role_name}' added successfully.")
    except Exception as e:
        st.error(f"Error adding role: {e}")
    finally:
        conn.close()

def update_role(role_id, new_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE admin_roles SET role_name = %s WHERE role_id = %s", (new_name, role_id))
        conn.commit()
        st.success(f"✏️ Role updated to '{new_name}'.")
    except Exception as e:
        st.error(f"Error updating role: {e}")
    finally:
        conn.close()

def delete_role(role_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM admin_roles WHERE role_id = %s", (role_id,))
        conn.commit()
        st.success("🗑️ Role deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting role: {e}")
    finally:
        conn.close()

# ------------------------------
# Streamlit UI for roles
# ------------------------------

def show_roles_dashboard():
    st.title("🛡️ Admin Roles Management")

    # Show existing roles
    st.subheader("📋 Existing Roles")
    roles = fetch_roles()
    if roles:
        st.table(roles)
    else:
        st.info("No roles found.")

    st.divider()

    # Add role
    st.subheader("➕ Add New Role")
    new_role = st.text_input("Role Name")
    if st.button("Add Role"):
        if new_role.strip():
            add_role(new_role.strip())
        else:
            st.warning("Please enter a valid role name.")

    st.divider()

    # Update role
    st.subheader("✏️ Update Role")
    role_options = {str(r[0]): r[1] for r in roles}  # role_id -> role_name
    selected_role_id = st.selectbox("Select Role to Update", options=list(role_options.keys()))
    if selected_role_id:
        current_name = role_options[selected_role_id]
        updated_name = st.text_input("New Role Name", value=current_name)
        if st.button("Update Role"):
            if updated_name.strip():
                update_role(selected_role_id, updated_name.strip())
            else:
                st.warning("Role name cannot be empty.")

    st.divider()

    # Delete role
    st.subheader("❌ Delete Role")
    del_role_id = st.selectbox("Select Role to Delete", options=list(role_options.keys()), key="delete_role")
    if st.button("Delete Role"):
        delete_role(del_role_id)

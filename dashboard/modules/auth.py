# modules/auth.py
import streamlit as st
from config.db_config import get_cursor

def get_roles():
    cursor = get_cursor()
    cursor.execute("SELECT role_id, role_name FROM admin_roles ORDER BY role_name")
    roles = cursor.fetchall()
    return roles

def validate_login(email, password, role_id):
    """
    Check if email/password matches and role_id matches in admins table.
    Password here assumed plain for simplicity; replace with hashed check.
    """
    cursor = get_cursor()
    query = """
        SELECT admin_id, full_name, email, role_id 
        FROM admins 
        WHERE email = %s AND password = %s AND role_id = %s
    """
    cursor.execute(query, (email, password, role_id))
    user = cursor.fetchone()
    return user

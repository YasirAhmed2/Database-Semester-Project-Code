# modules/auth.py
import bcrypt
from config.db_config import get_cursor

ALLOWED_ROLE_IDS = {1, 3, 4, 5}  # admin=1, pilot=3, airline staff=4, security officer=5

def get_roles():
    cursor = get_cursor()
    cursor.execute("SELECT role_id, role_name FROM admin_roles WHERE role_id IN %s ORDER BY role_name", (tuple(ALLOWED_ROLE_IDS),))
    roles = cursor.fetchall()
    return roles

import bcrypt
from config.db_config import get_cursor

def validate_login(email, plain_password, role_id):
    """
    Authenticate user by email, hashed password, and role_id.
    Works for admin (1), pilot (2), airline staff (3), and security officer (4).
    """
    ALLOWED_ROLE_IDS = {1, 2, 3, 4}

    if role_id not in ALLOWED_ROLE_IDS:
        return None

    cursor = get_cursor()
    query = """
        SELECT admin_id, full_name, email, password, role_id 
        FROM admins 
        WHERE email = %s AND role_id = %s
    """
    cursor.execute(query, (email, role_id))
    user = cursor.fetchone()

    if not user:
        return None

    # RealDictCursor returns a dictionary
    stored_hashed_password = user['password']

    if bcrypt.checkpw(plain_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
        return {
            'admin_id': user['admin_id'],
            'full_name': user['full_name'],
            'email': user['email'],
            'role_id': user['role_id']
        }
    else:
        return None


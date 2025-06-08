import bcrypt
import psycopg2

# ---------------------------
# PASSWORD HASHING UTILITIES
# ---------------------------

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ---------------------------
# ROLE & USER UTILS
# ---------------------------

def get_user_by_email(conn, email: str):
    """
    Check if user exists in admins or passengers and return relevant data.
    """
    cur = conn.cursor()

    # Try Admins first
    cur.execute("""
        SELECT admin_id, full_name, email, password, role_id
        FROM admins
        WHERE email = %s
    """, (email,))
    admin = cur.fetchone()

    if admin:
        cur.execute("SELECT role_name FROM admin_roles WHERE role_id = %s", (admin[4],))
        role_name = cur.fetchone()[0] if cur.rowcount > 0 else "Admin"

        return {
            'user_id': admin[0],
            'name': admin[1],
            'email': admin[2],
            'hashed_password': admin[3],
            'role': role_name
        }

    # If not admin, check Passengers
    cur.execute("""
        SELECT passenger_id, full_name, email, passport_number
        FROM passengers
        WHERE email = %s
    """, (email,))
    passenger = cur.fetchone()

    if passenger:
        return {
            'user_id': passenger[0],
            'name': passenger[1],
            'email': passenger[2],
            'hashed_password': passenger[3],  # You may store passport number as fallback
            'role': 'Passenger'
        }

    return None  # No user found

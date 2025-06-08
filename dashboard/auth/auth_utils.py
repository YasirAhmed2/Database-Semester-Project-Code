# auth/auth_utils.py

import bcrypt
import psycopg2

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Role name to ID mapping
ROLE_MAP = {
    "Admin": 1,
    "Pilot": 2,
    "Security Officer": 3,
    "Customer": 4,
    "Airline Staff": 5
}

def get_user_by_email_and_role(conn, email: str, role: str):
    role_id = ROLE_MAP.get(role)

    if role_id is None:
        return None

    cur = conn.cursor()

    try:
        # All roles are stored in 'admins' table with different role_id
        cur.execute("""
            SELECT admin_id, full_name, email, password, role_id
            FROM admins
            WHERE email = %s AND role_id = %s
        """, (email, role_id))

        result = cur.fetchone()
        if result:
            user = {
                'user_id': result[0],
                'name': result[1],
                'email': result[2],
                'hashed_password': result[3],
                'role': role
            }
            return user

    except Exception as e:
        print("Error in get_user_by_email_and_role:", e)
        return None
    finally:
        cur.close()

    return None

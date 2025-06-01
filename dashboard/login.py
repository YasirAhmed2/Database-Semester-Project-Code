import bcrypt
from sqlalchemy import text

def login_user(session, email, password):
    # Get user record by email only
    result = session.execute(
        text("SELECT * FROM admins WHERE email = :email"),
        {"email": email}
    ).fetchone()

    if result:
        stored_hash = result.password  # assuming column name is 'password'
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return result

    return None

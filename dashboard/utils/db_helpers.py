import psycopg2
from psycopg2.extras import RealDictCursor
from config.db_config import get_db_connection

def fetch_all(query, params=None):
    """
    Fetch all rows for the given query.
    Returns list of dicts.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            results = cur.fetchall()
        return results
    except Exception as e:
        print(f"DB fetch_all error: {e}")
        return []
    finally:
        conn.close()

def fetch_one(query, params=None):
    """
    Fetch a single row for the given query.
    Returns dict or None.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            result = cur.fetchone()
        return result
    except Exception as e:
        print(f"DB fetch_one error: {e}")
        return None
    finally:
        conn.close()

def execute_query(query, params=None):
    """
    Execute insert, update, delete queries.
    Returns True if successful, False otherwise.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            conn.commit()
        return True
    except Exception as e:
        print(f"DB execute_query error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

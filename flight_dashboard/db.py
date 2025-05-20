# db.py
import psycopg2

# --- Replace with your actual credentials ---
DB_NAME = "AirportFlightManagement"
DB_USER = "yasir"
DB_PASS = "yasir1234"
DB_HOST = "localhost"  # or your DB server IP
DB_PORT = "6677"       # default PostgreSQL port

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def fetch_all(table_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    conn.close()
    return rows, colnames

def insert_record(table, columns, values):
    conn = get_connection()
    cur = conn.cursor()
    placeholders = ', '.join(['%s'] * len(values))
    query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    cur.execute(query, values)
    conn.commit()
    conn.close()

def update_record(table, column_values, condition):
    conn = get_connection()
    cur = conn.cursor()
    set_clause = ', '.join([f"{col} = %s" for col in column_values.keys()])
    where_clause = f"{condition[0]} = %s"
    values = list(column_values.values()) + [condition[1]]
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    cur.execute(query, values)
    conn.commit()
    conn.close()

def delete_record(table, condition):
    conn = get_connection()
    cur = conn.cursor()
    query = f"DELETE FROM {table} WHERE {condition[0]} = %s"
    cur.execute(query, (condition[1],))
    conn.commit()
    conn.close()

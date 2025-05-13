import psycopg2
from faker import Faker
import random
from tqdm import tqdm
import hashlib

fake = Faker()
# -------------------------- DB Setup ---------------------------
conn = psycopg2.connect(
    dbname="AirportFlightManagement",
    user="yasir",
    password="yasir1234",
    host="localhost",
    port="6677"
)
cursor = conn.cursor()

# ------------------- Step-by-Step Inserts ----------------------


def insert_airports(n=100000):
    print("Inserting airports...")
    airport_ids = []
    used_codes = set()  # To avoid duplicate codes

    for _ in tqdm(range(n)):
        name = f"{fake.city()} Airport"
        city = fake.city()
        country = fake.country()

        # Ensure code is unique
        while True:
            code = fake.lexify(text='????').upper()
            if code not in used_codes:
                used_codes.add(code)
                break

        cursor.execute("""
            INSERT INTO airports (name, city, country, code)
            VALUES (%s, %s, %s, %s)
            RETURNING airport_id
        """, (name, city, country, code))

        airport_ids.append(cursor.fetchone()[0])

    conn.commit()
    return airport_ids


def insert_terminals(airport_ids, terminals_per_airport=2):
    print("Inserting terminals...")
    terminal_ids = []
    for airport_id in tqdm(airport_ids):
        for i in range(terminals_per_airport):
            code = f"T{i+1}"
            cursor.execute("""
                INSERT INTO terminals (airport_id, terminal_code)
                VALUES (%s, %s)
                RETURNING terminal_id
            """, (airport_id, code))
            terminal_ids.append(cursor.fetchone()[0])
    conn.commit()
    return terminal_ids


def insert_gates(terminal_ids, gates_per_terminal=3):
    print("Inserting gates...")
    gate_ids = []
    for terminal_id in tqdm(terminal_ids):
        for i in range(gates_per_terminal):
            code = f"G{i+1}"
            cursor.execute("""
                INSERT INTO gates (terminal_id, gate_code)
                VALUES (%s, %s)
                RETURNING gate_id
            """, (terminal_id, code))
            gate_ids.append(cursor.fetchone()[0])
    conn.commit()
    return gate_ids


def insert_flight_statuses():
    print("Inserting flight statuses...\n")
    statuses = ['Scheduled', 'Cancelled', 'Delayed', 'Departed']
    for status in statuses:
        cursor.execute("""
            INSERT INTO flight_statuses (status_name)
            VALUES (%s)
            ON CONFLICT (status_name) DO NOTHING
        """, (status,))
    conn.commit()



def insert_payment_methods():
    print("Inserting payment methods...\n")
    methods = ['Credit Card', 'PayPal', 'Bank Transfer', 'Cash']
    for method in methods:
        cursor.execute("""
            INSERT INTO payment_methods (method_name)
            VALUES (%s)
            ON CONFLICT (method_name) DO NOTHING
        """, (method,))
    conn.commit()



def insert_booking_statuses():
    print("Inserting booking statuses...\n")
    statuses = ['Confirmed', 'Cancelled']
    for status in statuses:
        cursor.execute("""
            INSERT INTO booking_statuses (status_name)
            VALUES (%s)
            ON CONFLICT (status_name) DO NOTHING
        """, (status,))
    conn.commit()



def insert_passengers():
    print("Inserting passengers...\n")
    passenger_ids = []
    for _ in range(100000):  # Adjust the range as needed
        full_name = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()[:20]  # Ensure phone number is within 20 characters
        passport_number = fake.bothify(text='??????????????')[:20]  # Ensure passport number is within 20 characters
        nationality = fake.country()

        # Ensure all data fits within the expected lengths
        cursor.execute("""
            INSERT INTO passengers (full_name, email, phone_number, passport_number, nationality)
            VALUES (%s, %s, %s, %s, %s)
        """, (full_name, email, phone_number, passport_number, nationality))
        
        # Retrieve the inserted passenger ID
        cursor.execute("SELECT LASTVAL()")
        passenger_id = cursor.fetchone()[0]
        passenger_ids.append(passenger_id)

    conn.commit()
    return passenger_ids



def insert_flights(airport_ids, n=100000):
    print("Inserting flights...")
    cursor.execute("SELECT status_id FROM flight_statuses")
    status_ids = [row[0] for row in cursor.fetchall()]
    flight_ids = []
    for _ in tqdm(range(n)):
        origin, dest = random.sample(airport_ids, 2)
        flight_number = fake.unique.lexify(text='??###').upper()
        aircraft = random.choice(['Airbus A320', 'Boeing 737', 'Boeing 777'])
        status_id = random.choice(status_ids)
        cursor.execute("""
            INSERT INTO flights (flight_number, origin_airport_id, destination_airport_id, aircraft_type, status_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING flight_id
        """, (flight_number, origin, dest, aircraft, status_id))
        flight_ids.append(cursor.fetchone()[0])
    conn.commit()
    return flight_ids


def insert_flight_schedules(flight_ids, gate_ids):
    print("Inserting flight schedules...")
    schedule_ids = []
    for flight_id in tqdm(flight_ids):
        gate_id = random.choice(gate_ids)
        dep_time = fake.date_time_between(start_date='+1d', end_date='+10d')
        arr_time = fake.date_time_between(start_date=dep_time, end_date=dep_time.replace(hour=dep_time.hour + 3))
        cursor.execute("""
            INSERT INTO flight_schedules (flight_id, departure_time, arrival_time, gate_id)
            VALUES (%s, %s, %s, %s)
            RETURNING schedule_id
        """, (flight_id, dep_time, arr_time, gate_id))
        schedule_ids.append(cursor.fetchone()[0])
    conn.commit()
    return schedule_ids


def insert_admin_roles():
    roles = ['SuperAdmin', 'Manager', 'Staff']  # Example roles

    for role in roles:
        cursor.execute("""
            INSERT INTO admin_roles (role_name) 
            VALUES (%s) 
            ON CONFLICT (role_name) DO NOTHING
        """, (role,))
        print(f"Attempted to insert role: {role}")
    
    # Commit changes
    conn.commit()



def insert_admins(n=10):
    print("Inserting admins...")
    cursor.execute("SELECT role_id FROM admin_roles")
    role_ids = [row[0] for row in cursor.fetchall()]
    for _ in tqdm(range(n)):
        cursor.execute("""
            INSERT INTO admins (full_name, email, password, role_id)
            VALUES (%s, %s, %s, %s)
        """, (
            fake.name(),
            fake.unique.email(),
            hashlib.sha256("admin123".encode()).hexdigest(),
            random.choice(role_ids)
        ))
    conn.commit()


def insert_bookings(passenger_ids, schedule_ids):
    print("Inserting bookings...")
    cursor.execute("SELECT status_id FROM booking_statuses")
    status_ids = [row[0] for row in cursor.fetchall()]
    booking_ids = []
    for _ in tqdm(range(30)):
        cursor.execute("""
            INSERT INTO bookings (passenger_id, schedule_id, seat_number, status_id)
            VALUES (%s, %s, %s, %s)
            RETURNING booking_id
        """, (
            random.choice(passenger_ids),
            random.choice(schedule_ids),
            f"{random.randint(1, 30)}{random.choice(['A', 'B', 'C'])}",
            random.choice(status_ids)
        ))
        booking_ids.append(cursor.fetchone()[0])
    conn.commit()
    return booking_ids


def insert_payments(booking_ids):
    print("Inserting payments...")
    cursor.execute("SELECT method_id FROM payment_methods")
    method_ids = [row[0] for row in cursor.fetchall()]
    for booking_id in tqdm(booking_ids):
        cursor.execute("""
            INSERT INTO payments (booking_id, amount, method_id)
            VALUES (%s, %s, %s)
        """, (
            booking_id,
            round(random.uniform(100.0, 1000.0), 2),
            random.choice(method_ids)
        ))
    conn.commit()


def insert_notifications(passenger_ids):
    print("Inserting notifications...")
    for _ in tqdm(range(20)):
        cursor.execute("""
            INSERT INTO notifications (passenger_id, message)
            VALUES (%s, %s)
        """, (random.choice(passenger_ids), fake.sentence()))
    conn.commit()

# ------------------ Run Everything ---------------------------

if __name__ == "__main__":
    airport_ids = insert_airports()
    terminal_ids = insert_terminals(airport_ids)
    gate_ids = insert_gates(terminal_ids)

    insert_flight_statuses()
    insert_payment_methods()
    insert_booking_statuses()

    passenger_ids = insert_passengers()
    insert_admin_roles()
    insert_admins()

    flight_ids = insert_flights(airport_ids)
    schedule_ids = insert_flight_schedules(flight_ids, gate_ids)

    booking_ids = insert_bookings(passenger_ids, schedule_ids)
    insert_payments(booking_ids)
    insert_notifications(passenger_ids)

    print("All dummy data inserted successfully!")

    cursor.close()
    conn.close()

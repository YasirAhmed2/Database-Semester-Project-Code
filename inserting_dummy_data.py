import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Database connection parameters
DB_NAME = "AirportFlightManagement"
DB_USER = "yasir"
DB_PASSWORD = "yasir1234"
DB_HOST = "localhost"
DB_PORT = "6677"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Set the number of records you want (adjust as needed)
NUM_RECORDS = 100000  # For 100k records, adjust based on our system capabilities

def create_dummy_data():
    print("Starting dummy data generation...")
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    cursor.execute("""
        TRUNCATE TABLE notifications, payments, bookings, flight_schedules, flights, 
        passengers, booking_statuses, payment_methods, flight_statuses, 
        gates, terminals, airports, admins, admin_roles CASCADE;
    """)
    conn.commit()
    
    # 1. Create flight statuses
    flight_statuses = ['Scheduled', 'Cancelled', 'Delayed', 'Departed']
    for status in flight_statuses:
        cursor.execute("INSERT INTO flight_statuses (status_name) VALUES (%s)", (status,))
    conn.commit()
    
    # # 2. Create booking statuses
    booking_statuses = ['Confirmed', 'Cancelled']
    for status in booking_statuses:
        cursor.execute("INSERT INTO booking_statuses (status_name) VALUES (%s)", (status,))
    conn.commit()
    
    # # 3. Create payment methods
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cryptocurrency']
    for method in payment_methods:
        cursor.execute("INSERT INTO payment_methods (method_name) VALUES (%s)", (method,))
    conn.commit()
    
    # # 4. Create admin roles
    admin_roles = ['SuperAdmin', 'Manager', 'Staff']
    for role in admin_roles:
        cursor.execute("INSERT INTO admin_roles (role_name) VALUES (%s)", (role,))
    conn.commit()
    
    # 5. Create airports (100 major airports worldwide)
    print("Creating airports...")
    airports_data = []
    for _ in range(100):
        city = fake.city()
        country = fake.country()
        code = fake.unique.lexify(text='???', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        name = f"{city} International Airport"
        airports_data.append((name, city, country, code))
    
    cursor.executemany(
        "INSERT INTO airports (name, city, country, code) VALUES (%s, %s, %s, %s)",
        airports_data
    )
    conn.commit()
    
    # # Get all airport IDs
    cursor.execute("SELECT airport_id FROM airports")
    airport_ids = [row[0] for row in cursor.fetchall()]
    
    # 6. Create terminals (3-5 per airport)
    print("Creating terminals...")
    terminals_data = []
    for airport_id in airport_ids:
        num_terminals = random.randint(3, 5)
        for i in range(1, num_terminals + 1):
            terminal_code = f"T{i}"
            terminals_data.append((airport_id, terminal_code))
    
    cursor.executemany(
        "INSERT INTO terminals (airport_id, terminal_code) VALUES (%s, %s)",
        terminals_data
    )
    conn.commit()
    
    # Get all terminal IDs
    cursor.execute("SELECT terminal_id FROM terminals")
    terminal_ids = [row[0] for row in cursor.fetchall()]
    
    # 7. Create gates (10-20 per terminal)
    print("Creating gates...")
    gates_data = []
    for terminal_id in terminal_ids:
        num_gates = random.randint(10, 20)
        for i in range(1, num_gates + 1):
            gate_code = f"{terminal_id}{chr(64 + i)}"  # A, B, C, etc.
            gates_data.append((terminal_id, gate_code))
    
    cursor.executemany(
        "INSERT INTO gates (terminal_id, gate_code) VALUES (%s, %s)",
        gates_data
    )
    conn.commit()
    
    # Get all gate IDs
    cursor.execute("SELECT gate_id FROM gates")
    gate_ids = [row[0] for row in cursor.fetchall()]
    
    # 8. Create flights
    print("Creating flights...")
    flights_data = []
    aircraft_types = ['Boeing 737', 'Boeing 747', 'Airbus A320', 'Airbus A380', 'Embraer E190']
    
    for _ in range(NUM_RECORDS ):  # Adjust based on your needs
        flight_number = fake.unique.bothify(text='??####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        origin = random.choice(airport_ids)
        destination = random.choice([aid for aid in airport_ids if aid != origin])
        aircraft = random.choice(aircraft_types)
        status = random.randint(1, len(flight_statuses))
        flights_data.append((flight_number, origin, destination, aircraft, status))
    
    cursor.executemany(
        """INSERT INTO flights (flight_number, origin_airport_id, destination_airport_id, 
           aircraft_type, status_id) VALUES (%s, %s, %s, %s, %s)""",
        flights_data
    )
    conn.commit()
    
    # Get all flight IDs
    cursor.execute("SELECT flight_id FROM flights")
    flight_ids = [row[0] for row in cursor.fetchall()]
    
    # 9. Create flight schedules
    print("Creating flight schedules...")
    schedules_data = []
    
    for flight_id in flight_ids:
        # Create 1-3 schedules per flight
        for _ in range(random.randint(1, 3)):
            departure_time = fake.date_time_between(start_date='-30d', end_date='+90d')
            flight_duration = timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + flight_duration
            gate_id = random.choice(gate_ids)
            schedules_data.append((flight_id, departure_time, arrival_time, gate_id))
    
    cursor.executemany(
        """INSERT INTO flight_schedules (flight_id, departure_time, arrival_time, gate_id) 
           VALUES (%s, %s, %s, %s)""",
        schedules_data
    )
    conn.commit()
    
    # Get all schedule IDs
    cursor.execute("SELECT schedule_id FROM flight_schedules")
    schedule_ids = [row[0] for row in cursor.fetchall()]
    
    # 10. Create passengers
    print("Creating passengers...")
    passengers_data = []
    for _ in range(NUM_RECORDS):
        full_name = fake.name()
        email = fake.unique.email()
        phone = fake.phone_number()[:20]
        passport = fake.unique.bothify(text='??#######', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        nationality = fake.country()
        passengers_data.append((full_name, email, phone, passport, nationality))
    
    cursor.executemany(
        """INSERT INTO passengers (full_name, email, phone_number, passport_number, nationality) 
           VALUES (%s, %s, %s, %s, %s)""",
        passengers_data
    )
    conn.commit()
    
    # Get all passenger IDs
    cursor.execute("SELECT passenger_id FROM passengers")
    passenger_ids = [row[0] for row in cursor.fetchall()]
    
    # 11. Create bookings
    print("Creating bookings...")
    bookings_data = []
    seat_rows = range(1, 40)
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    
    for _ in range(NUM_RECORDS):
        passenger_id = random.choice(passenger_ids)
        schedule_id = random.choice(schedule_ids)
        seat_number = f"{random.choice(seat_rows)}{random.choice(seat_letters)}"
        status_id = random.randint(1, len(booking_statuses))
        booked_at = fake.date_time_between(start_date='-60d', end_date='now')
        bookings_data.append((passenger_id, schedule_id, seat_number, status_id, booked_at))
    
    cursor.executemany(
        """INSERT INTO bookings (passenger_id, schedule_id, seat_number, status_id, booked_at) 
           VALUES (%s, %s, %s, %s, %s)""",
        bookings_data
    )
    conn.commit()
    
    # Get all booking IDs
    cursor.execute("SELECT booking_id FROM bookings")
    booking_ids = [row[0] for row in cursor.fetchall()]
    
    # 12. Create payments
    print("Creating payments...")
    payments_data = []
    
    for booking_id in booking_ids:
        amount = round(random.uniform(100, 2000), 2)
        method_id = random.randint(1, len(payment_methods))
        payment_status = 'Completed' if random.random() > 0.1 else 'Failed'
        payment_date = fake.date_time_between(start_date='-60d', end_date='now')
        payments_data.append((booking_id, amount, method_id, payment_status, payment_date))
    
    cursor.executemany(
        """INSERT INTO payments (booking_id, amount, method_id, payment_status, payment_date) 
           VALUES (%s, %s, %s, %s, %s)""",
        payments_data
    )
    conn.commit()
    
    # 13. Create admins
    print("Creating admins...")
    admins_data = []
    for _ in range(20):  # Creating 20 admin accounts
        full_name = fake.name()
        email = fake.unique.email()
        password = "hashed_password_placeholder"  # In real app, use proper password hashing
        role_id = random.randint(1, len(admin_roles))
        admins_data.append((full_name, email, password, role_id))
    
    cursor.executemany(
        """INSERT INTO admins (full_name, email, password, role_id) 
           VALUES (%s, %s, %s, %s)""",
        admins_data
    )
    conn.commit()
    
    # 14. Create notifications
    print("Creating notifications...")
    notifications_data = []
    messages = [
        "Your flight has been confirmed",
        "Your flight is delayed by 1 hour",
        "Gate change for your flight",
        "Your booking has been cancelled",
        "Check-in is now open for your flight",
        "Your payment was successful",
        "Boarding has begun for your flight"
    ]
    
    for _ in range(NUM_RECORDS ):  # Adjust based on your needs
        passenger_id = random.choice(passenger_ids)
        message = random.choice(messages)
        sent_at = fake.date_time_between(start_date='-60d', end_date='now')
        notifications_data.append((passenger_id, message, sent_at))
    
    cursor.executemany(
        """INSERT INTO notifications (passenger_id, message, sent_at) 
           VALUES (%s, %s, %s)""",
        notifications_data
    )
    conn.commit()
    
    print("Dummy data generation completed successfully!")

if __name__ == "__main__":
    try:
        create_dummy_data()
    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
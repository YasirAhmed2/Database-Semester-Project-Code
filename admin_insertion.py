import psycopg2
import bcrypt
from faker import Faker
import random
# Connect to PostgreSQL (update your credentials here)
conn = psycopg2.connect(
    dbname="AirportFlightManagement",
    user="yasir",
    password="yasir1234",
    host="localhost",
    port="6677"
)
cursor = conn.cursor()
admin_roles = ['Admin','Passenger','Pilot','Airline Staff','Security Officer']
# for role in admin_roles:
#     cursor.execute("INSERT INTO admin_roles (role_name) VALUES (%s)", (role,))
#     conn.commit()
fake=Faker()
# Admin details
# full_name = "Super Admin"
# email = "superadmin@example.com"
# password = "admin123"  # plain text password
# role_id = 1  # assuming 1 = SuperAdmin

print("Creating admins...")
admins_data = []
for _ in range(1000):  # Creating 20 admin accounts
    full_name = fake.name()
    email = fake.unique.email()
    raw_password="admin12345"
    password =  bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') # In real app, use proper password hashing
    role_id = random.randint(1, len(admin_roles))
    admins_data.append((full_name, email, password, role_id))
    cursor.execute("""
    INSERT INTO admins (full_name, email, password, role_id)
    VALUES (%s, %s, %s, %s)
""", (full_name, email, password, role_id))

conn.commit()

# Hash the password


# Insert into the admins table

print("Admin inserted with hashed password.")
cursor.close()
conn.close()

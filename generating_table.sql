--  Airports
CREATE TABLE airports (
    airport_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    code VARCHAR(10) UNIQUE NOT NULL -- e.g. LAX, JFK
);

--  Terminals (associated with airport)
CREATE TABLE terminals (
    terminal_id SERIAL PRIMARY KEY,
    airport_id INT REFERENCES airports(airport_id),
    terminal_code VARCHAR(10) NOT NULL
);

--  Gates (associated with terminal)
CREATE TABLE gates (
    gate_id SERIAL PRIMARY KEY,
    terminal_id INT REFERENCES terminals(terminal_id),
    gate_code VARCHAR(10) NOT NULL
);

--  Flight Status Types
CREATE TABLE flight_statuses (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(20) UNIQUE -- Scheduled, Cancelled, Delayed, Departed
);

--  Payment Methods
CREATE TABLE payment_methods (
    method_id SERIAL PRIMARY KEY,
    method_name VARCHAR(50) UNIQUE -- Credit Card, PayPal, etc.
);

--  Booking Statuses
CREATE TABLE booking_statuses (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(20) UNIQUE -- Confirmed, Cancelled
);

--  Passengers
CREATE TABLE passengers (
    passenger_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(20),
    passport_number VARCHAR(20) UNIQUE,
    nationality VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Flights (generic info)
CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_number VARCHAR(10) UNIQUE,
    origin_airport_id INT REFERENCES airports(airport_id),
    destination_airport_id INT REFERENCES airports(airport_id),
    aircraft_type VARCHAR(50),
    status_id INT REFERENCES flight_statuses(status_id) DEFAULT 1
);

--  Flight Schedules (with time and location)
CREATE TABLE flight_schedules (
    schedule_id SERIAL PRIMARY KEY,
    flight_id INT REFERENCES flights(flight_id),
    departure_time TIMESTAMP,
    arrival_time TIMESTAMP,
    gate_id INT REFERENCES gates(gate_id)
);

--  Bookings
CREATE TABLE bookings (
    booking_id SERIAL PRIMARY KEY,
    passenger_id INT REFERENCES passengers(passenger_id),
    schedule_id INT REFERENCES flight_schedules(schedule_id),
    seat_number VARCHAR(10),
    status_id INT REFERENCES booking_statuses(status_id) DEFAULT 1,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Payments
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INT REFERENCES bookings(booking_id),
    amount DECIMAL(10, 2),
    method_id INT REFERENCES payment_methods(method_id),
    payment_status VARCHAR(20) DEFAULT 'Completed', -- consider replacing with a status table
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--  Admin Roles (optional for RBAC)
CREATE TABLE admin_roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE -- SuperAdmin, Manager, Staff
);

--  Admins
CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255), -- store hashed password only
    role_id INT REFERENCES admin_roles(role_id)
);

--  Notifications
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    passenger_id INT REFERENCES passengers(passenger_id),
    message TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, DECIMAL, Text
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Airport(Base):
    __tablename__ = "airports"
    airport_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    code = Column(String(10), unique=True, nullable=False)

    terminals = relationship("Terminal", back_populates="airport")
    flights_origin = relationship("Flight", back_populates="origin_airport", foreign_keys='Flight.origin_airport_id')
    flights_destination = relationship("Flight", back_populates="destination_airport", foreign_keys='Flight.destination_airport_id')


class Terminal(Base):
    __tablename__ = "terminals"
    terminal_id = Column(Integer, primary_key=True, index=True)
    airport_id = Column(Integer, ForeignKey("airports.airport_id"))
    terminal_code = Column(String(10), nullable=False)

    airport = relationship("Airport", back_populates="terminals")
    gates = relationship("Gate", back_populates="terminal")


class Gate(Base):
    __tablename__ = "gates"
    gate_id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(Integer, ForeignKey("terminals.terminal_id"))
    gate_code = Column(String(10), nullable=False)

    terminal = relationship("Terminal", back_populates="gates")
    flight_schedules = relationship("FlightSchedule", back_populates="gate")


class FlightStatus(Base):
    __tablename__ = "flight_statuses"
    status_id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(20), unique=True)

    flights = relationship("Flight", back_populates="status")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    method_id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String(50), unique=True)

    payments = relationship("Payment", back_populates="method")


class BookingStatus(Base):
    __tablename__ = "booking_statuses"
    status_id = Column(Integer, primary_key=True, index=True)
    status_name = Column(String(20), unique=True)

    bookings = relationship("Booking", back_populates="status")


class Passenger(Base):
    __tablename__ = "passengers"
    passenger_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
    passport_number = Column(String(20), unique=True)
    nationality = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship("Booking", back_populates="passenger")
    notifications = relationship("Notification", back_populates="passenger")


class Flight(Base):
    __tablename__ = "flights"
    flight_id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(10), unique=True)
    origin_airport_id = Column(Integer, ForeignKey("airports.airport_id"))
    destination_airport_id = Column(Integer, ForeignKey("airports.airport_id"))
    aircraft_type = Column(String(50))
    status_id = Column(Integer, ForeignKey("flight_statuses.status_id"), default=1)

    origin_airport = relationship("Airport", foreign_keys=[origin_airport_id], back_populates="flights_origin")
    destination_airport = relationship("Airport", foreign_keys=[destination_airport_id], back_populates="flights_destination")
    status = relationship("FlightStatus", back_populates="flights")
    schedules = relationship("FlightSchedule", back_populates="flight")


class FlightSchedule(Base):
    __tablename__ = "flight_schedules"
    schedule_id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, ForeignKey("flights.flight_id"))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    gate_id = Column(Integer, ForeignKey("gates.gate_id"))

    flight = relationship("Flight", back_populates="schedules")
    gate = relationship("Gate", back_populates="flight_schedules")
    bookings = relationship("Booking", back_populates="schedule")


class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.passenger_id"))
    schedule_id = Column(Integer, ForeignKey("flight_schedules.schedule_id"))
    seat_number = Column(String(10))
    status_id = Column(Integer, ForeignKey("booking_statuses.status_id"), default=1)
    booked_at = Column(DateTime(timezone=True), server_default=func.now())

    passenger = relationship("Passenger", back_populates="bookings")
    schedule = relationship("FlightSchedule", back_populates="bookings")
    status = relationship("BookingStatus", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking")


class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.booking_id"))
    amount = Column(DECIMAL(10, 2))
    method_id = Column(Integer, ForeignKey("payment_methods.method_id"))
    payment_status = Column(String(20), default="Completed")
    payment_date = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="payments")
    method = relationship("PaymentMethod", back_populates="payments")


class AdminRole(Base):
    __tablename__ = "admin_roles"
    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True)

    admins = relationship("Admin", back_populates="role")


class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))  # Hashed password
    role_id = Column(Integer, ForeignKey("admin_roles.role_id"))

    role = relationship("AdminRole", back_populates="admins")


class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    passenger_id = Column(Integer, ForeignKey("passengers.passenger_id"))
    message = Column(Text)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

    passenger = relationship("Passenger", back_populates="notifications")

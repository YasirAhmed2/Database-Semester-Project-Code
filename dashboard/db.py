# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://yasir:yasir1234@localhost:6677/AirportFlightManagement"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

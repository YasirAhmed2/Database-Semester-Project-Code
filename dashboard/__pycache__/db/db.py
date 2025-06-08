from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace these values with your actual database credentials
DB_USER = "yasir"
DB_PASSWORD = "yasir12345"
DB_HOST = "localhost"
DB_PORT = "6677"
DB_NAME = "AirportFlightManagement"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL query logging, set False in production

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit
Base = declarative_base()

# Dependency to get DB session for use (like FastAPI style)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

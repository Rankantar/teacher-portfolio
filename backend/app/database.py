import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Database URL from environment variables with default fallback
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/teacher_db")

# SQLAlchemy setup
try:
    # Try to connect to the configured database (PostgreSQL in Docker)
    engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
    # Test the connection
    with engine.connect() as conn:
        pass
    print("Connected to PostgreSQL database")
except OperationalError:
    # Fallback to SQLite for local development
    print("Could not connect to PostgreSQL, falling back to SQLite")
    SQLITE_URL = "sqlite:///./teacher_portfolio.db"
    engine = create_engine(
        SQLITE_URL, 
        connect_args={"check_same_thread": False}
    )
    print(f"Using SQLite database at {SQLITE_URL}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
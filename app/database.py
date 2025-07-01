# app/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Database Setup ---

# creating a file named 'robot_trajectories.db' in the project's root directory.
DATABASE_URL = "sqlite:///./robot_trajectories.db"


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


# A 'SessionLocal' class is a factory for creating new database sessions.
# Think of a session as a temporary conversation with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 'Base' is a class that our database model will inherit from.
# SQLAlchemy uses this base class to map our Python objects to database tables.
Base = declarative_base()


# --- Dependency for FastAPI ---
def get_db():
    """
    This is a dependency function for FastAPI.
    It creates a new database session for each incoming request,
    and makes sure to close the session when the request is finished.
    This is a standard and safe pattern for database operations in web APIs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def create_database_and_tables():
    """
    A utility function to create the database file and all tables.
    We call this once when our application starts up.
    """
    # This checks if the database file already exists. If it does, we don't
    # want to accidentally delete it. For this simple assignment, we can just
    # ensure we don't re-create things, but in a real app you'd use migrations.
    if not os.path.exists(DATABASE_URL.split("///")[1]):
        print("Creating database and tables...")
        Base.metadata.create_all(bind=engine)
        print("Database and tables created.")
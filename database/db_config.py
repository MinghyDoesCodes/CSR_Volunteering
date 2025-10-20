"""
Database Configuration Module
Handles SQLAlchemy setup and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Database file location
DATABASE_URL = "sqlite:///csr_volunteering.db"

# Create database engine
# echo=True prints SQL queries (useful for learning/debugging)
engine = create_engine(DATABASE_URL, echo=False)

# Base class for all Entity models
Base = declarative_base()

# Session factory for database operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Thread-safe session
session = scoped_session(SessionLocal)

def get_session():
    """
    Get a database session
    Returns a session object for database operations
    """
    return session

def close_session():
    """
    Close the current database session
    """
    session.remove()

def init_database():
    """
    Initialize database - create all tables
    This reads all Entity classes and creates corresponding tables
    """
    # Import all entity models so they're registered with Base
    from entities.user_account import UserAccount
    from entities.user_profile import UserProfile
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
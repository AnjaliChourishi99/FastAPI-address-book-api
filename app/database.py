"""
Database configuration and session management.
Uses SQLite for persistent storage of addresses.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logger = logging.getLogger(__name__)

# SQLite database URL - creates a file named 'address_book.db' in the project root
SQLALCHEMY_DATABASE_URL = "sqlite:///./address_book.db"

# Create SQLAlchemy engine
# check_same_thread=False is needed for SQLite to work with FastAPI's async nature
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL query logging during development
)

# SessionLocal class - each instance will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    """
    db = SessionLocal()
    try:
        logger.debug("Database session created")
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")


def init_db():
    """
    Initialize the database by creating all tables.
    Should be called on application startup.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


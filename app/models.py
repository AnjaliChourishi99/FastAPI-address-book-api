"""
SQLAlchemy ORM models for the Address Book application.
Defines the database table structure for addresses.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Address(Base):
    """
    Address model representing a location in the address book.
    
    Attributes:
        id: Unique identifier for the address
        street: Street name and number
        city: City name
        state: State or province
        country: Country name
        postal_code: Postal/ZIP code
        latitude: Geographic latitude coordinate (-90 to 90)
        longitude: Geographic longitude coordinate (-180 to 180)
        created_at: Timestamp when the address was created
        updated_at: Timestamp when the address was last updated
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    street = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=True)
    country = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=True)
    
    # Geographic coordinates for location-based queries
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    
    # Timestamps for tracking changes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}', country='{self.country}')>"



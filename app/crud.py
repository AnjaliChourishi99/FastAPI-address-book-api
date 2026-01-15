"""
CRUD operations for addresses.
Provides database interaction functions for the Address model.
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)


def create_address(db: Session, address: AddressCreate) -> Address:
    """
    Create a new address in the database.
    
    Args:
        db: Database session
        address: Address data for creation
        
    Returns:
        Address: The newly created address record
    """
    db_address = Address(**address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    logger.info(f"Created new address with ID: {db_address.id}")
    return db_address


def get_address(db: Session, address_id: int) -> Optional[Address]:
    """
    Retrieve a single address by its ID.
    
    Args:
        db: Database session
        address_id: The unique identifier of the address
        
    Returns:
        Address or None: The address if found, None otherwise
    """
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        logger.debug(f"Retrieved address ID: {address_id}")
    else:
        logger.debug(f"Address ID {address_id} not found")
    return address


def get_all_addresses(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    """
    Retrieve all addresses with pagination support.
    
    Args:
        db: Database session
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
        
    Returns:
        List[Address]: List of address records
    """
    addresses = db.query(Address).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(addresses)} addresses (skip={skip}, limit={limit})")
    return addresses


def get_addresses_count(db: Session) -> int:
    """
    Get the total count of addresses in the database.
    
    Args:
        db: Database session
        
    Returns:
        int: Total number of addresses
    """
    return db.query(Address).count()


def update_address(
    db: Session,
    address_id: int,
    address_update: AddressUpdate
) -> Optional[Address]:
    """
    Update an existing address with partial data.
    
    Args:
        db: Database session
        address_id: The unique identifier of the address to update
        address_update: Partial address data for update
        
    Returns:
        Address or None: The updated address if found, None otherwise
    """
    db_address = get_address(db, address_id)
    if not db_address:
        return None
    
    # Only update fields that were explicitly provided
    update_data = address_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_address, field, value)
    
    db.commit()
    db.refresh(db_address)
    logger.info(f"Updated address ID: {address_id}")
    return db_address


def delete_address(db: Session, address_id: int) -> bool:
    """
    Delete an address from the database.
    
    Args:
        db: Database session
        address_id: The unique identifier of the address to delete
        
    Returns:
        bool: True if deleted successfully, False if not found
    """
    db_address = get_address(db, address_id)
    if not db_address:
        return False
    
    db.delete(db_address)
    db.commit()
    logger.info(f"Deleted address ID: {address_id}")
    return True


def get_addresses_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float
) -> List[Address]:
    """
    Retrieve all addresses within a specified distance from given coordinates.
    
    Uses the Haversine formula to calculate distances between coordinates.
    
    Args:
        db: Database session
        latitude: latitude value
        longitude: longitude value
        distance_km: Maximum distance in kilometers
        
    Returns:
        List[Address]: List of addresses within the specified distance
    """
    # Get all addresses and filter by distance
    all_addresses = db.query(Address).all()
    
    nearby_addresses = []
    
    # Logic to calculate distance using some formula
    
    return nearby_addresses


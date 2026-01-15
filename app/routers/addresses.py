"""
Address API Router.
Provides endpoints for CRUD operations and location-based queries on addresses.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    AddressCreate,
    AddressUpdate,
    AddressResponse,
    AddressListResponse,
    MessageResponse
)
from app import crud

logger = logging.getLogger(__name__)

# Create router with prefix and tags for OpenAPI documentation
router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


@router.post(
    "/",
    response_model=AddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Create a new address in the address book.
    """
    logger.info(f"Creating new address in {address.city}, {address.country}")
    db_address = crud.create_address(db=db, address=address)
    return db_address


@router.get(
    "/",
    response_model=AddressListResponse,
)
def list_addresses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
    db: Session = Depends(get_db)
) -> AddressListResponse:
    """
    Retrieve all addresses with pagination support.
    """
    addresses = crud.get_all_addresses(db=db, skip=skip, limit=limit)
    total = crud.get_addresses_count(db=db)
    logger.debug(f"Listing addresses: returning {len(addresses)} of {total} total")
    return AddressListResponse(total=total, addresses=addresses)


@router.get(
    "/{address_id}",
    response_model=AddressResponse,
)
def get_address(
    address_id: int,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Retrieve a single address by its ID.
    - address_id: The unique identifier of the address
    """
    db_address = crud.get_address(db=db, address_id=address_id)
    if db_address is None:
        logger.warning(f"Address ID {address_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return db_address


@router.put(
    "/{address_id}",
    response_model=AddressResponse,
)
def update_address(
    address_id: int,
    address_update: AddressUpdate,
    db: Session = Depends(get_db)
) -> AddressResponse:
    """
    Update an existing address with partial data.
    
    - address_id: The unique identifier of the address to update
    - Only fields provided in the request body will be updated
    """
    logger.info(f"Updating address ID: {address_id}")
    db_address = crud.update_address(
        db=db,
        address_id=address_id,
        address_update=address_update
    )
    if db_address is None:
        logger.warning(f"Address ID {address_id} not found for update")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return db_address


@router.delete(
    "/{address_id}",
    response_model=MessageResponse,
)
def delete_address(
    address_id: int,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Delete an address by its ID.
    
    - address_id: The unique identifier of the address to delete
    """
    logger.info(f"Deleting address ID: {address_id}")
    success = crud.delete_address(db=db, address_id=address_id)
    if not success:
        logger.warning(f"Address ID {address_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return MessageResponse(
        message="Address deleted successfully",
        detail=f"Address ID {address_id} has been removed"
    )


@router.get(
    "/search/nearby",
    response_model=List[AddressResponse],
)
def find_nearby_addresses(
    latitude: float = Query(..., ge=-90, le=90, description="Center point latitude"),
    longitude: float = Query(..., ge=-180, le=180, description="Center point longitude"),
    distance_km: float = Query(..., gt=0, le=20000, description="Search radius in km"),
    db: Session = Depends(get_db)
) -> List[AddressResponse]:
    """
    Search for addresses within a specified distance (using GET with query parameters).
    
    Alternative endpoint that accepts search parameters via query string.
    Useful for simple testing and browser-based API exploration.
    """
    logger.info(
        f"GET search: addresses within {distance_km}km of ({latitude}, {longitude})"
    )
    addresses = crud.get_addresses_within_distance(
        db=db,
        latitude=latitude,
        longitude=longitude,
        distance_km=distance_km
    )
    return addresses


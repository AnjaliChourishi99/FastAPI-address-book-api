"""Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class AddressCreate(BaseModel):
    """Schema for creating address."""
    street: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["123 Main Street"]
    )
    city: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Indore"]
    )
    state: Optional[str] = Field(
        None,
        max_length=100,
        examples=["MP"]
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["India"]
    )
    postal_code: Optional[str] = Field(
        None,
        max_length=20,
        examples=["452000"]
    )
    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude coordinate (-90 to 90)",
        examples=[20.7128]
    )
    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude coordinate (-180 to 180)",
        examples=[-114.0060]
    )

    @field_validator('street', 'city', 'country')
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Remove leading/trailing whitespace from string fields."""
        return v.strip() if v else v


class AddressUpdate(BaseModel):
    """Schema for updating address - all fields optional."""
    street: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)

    @field_validator('street', 'city', 'country')
    @classmethod
    def strip_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Remove leading/trailing whitespace from string fields."""
        return v.strip() if v else v


class AddressResponse(BaseModel):
    """Schema for address response."""
    id: int
    street: str
    city: str
    state: Optional[str]
    country: str
    postal_code: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AddressListResponse(BaseModel):
    """Schema for paginated address list."""
    total: int
    addresses: List[AddressResponse]


class NearbySearchRequest(BaseModel):
    """Schema for nearby search."""
    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Center point latitude",
        examples=[40.7128]
    )
    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Center point longitude",
        examples=[-74.0060]
    )
    distance_km: float = Field(
        ...,
        gt=0,
        le=20000,
        description="Search radius in kilometers",
        examples=[10.0]
    )


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None

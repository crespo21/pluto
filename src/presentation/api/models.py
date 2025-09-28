"""Pydantic models for API requests and responses."""

from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for user creation requests."""
    
    username: str = Field(..., min_length=3, max_length=50, description="Unique username for the user")
    email: str = Field(..., max_length=100, description="Valid email address")
    status: str = Field(default="active", description="User status (active, inactive, pending, banned)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "status": "active"
            }
        }
    }


class UserResponse(BaseModel):
    """Schema for user responses."""
    
    id: Optional[int] = None
    username: str
    email: str
    status: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "status": "active"
            }
        }
    }


class UserPartialUpdate(BaseModel):
    """Schema for partial user updates."""
    
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="New username (optional)")
    email: Optional[str] = Field(None, max_length=100, description="New email address (optional)")
    status: Optional[str] = Field(None, description="New status (optional)")


class UserStatusUpdate(BaseModel):
    """Schema for user status updates."""
    
    status: str = Field(..., description="New status value (active, inactive, pending, banned)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "inactive"
            }
        }
    }
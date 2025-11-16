"""Pydantic models for API requests and responses."""

from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


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
    
    user_id: Optional[int] = None
    username: str
    email: str
    status: str
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
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

class ProductCreate(BaseModel):
    """Schema for product creation requests."""
  
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: Decimal = Field(..., gt=0, description="Product price (must be positive)")
    description: str = Field(default="", max_length=500, description="Product description")
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Laptop",
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class ProductResponse(BaseModel):
    """Schema for product responses."""
  
    product_id: Optional[int] = None
    name: str
    price: Decimal
    description: str
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "product_id": 1,
                "name": "Laptop", 
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class ProductUpdate(BaseModel):
    """Schema for product updates."""
  
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)

class CategoryCreate(BaseModel):
    """Schema for category creation requests."""
  
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: str = Field(default="", max_length=500, description="Category description")
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Electronics",
                "description": "Category for electronic products"
            }
        }
    }

class CategoryResponse(BaseModel):
    """Schema for category responses."""
  
    category_id: Optional[int] = None
    name: str
    description: str
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "category_id": 1,
                "name": "Electronics", 
                "description": "Category for electronic products"
            }
        }
    }

class CategoryUpdate(BaseModel):
    """Schema for category updates."""
  
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

    
class CartAddRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="ID of the user adding to cart")
    name: str = Field(..., min_length=1, max_length=100, description="Product name")
    price: Decimal = Field(..., gt=0, description="Product price (must be positive)")
    description: str = Field(default="", max_length=500, description="Product description")
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v is None or v <= 0:
            raise ValueError("user_id must be a positive integer")
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("name cannot be empty or whitespace")
        return v.strip()
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("price must be greater than 0")
        return v
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "name": "Laptop",
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class CartResponse(BaseModel):
    """Schema for cart responses."""
    id: Optional[int] = None
    user_id: int
    product_id: Optional[int] = None
    name: str
    price: Decimal
    description: str
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "user_id": 1,
                "product_id": 2,
                "name": "Laptop", 
                "price": 999.99,
                "description": "High-performance laptop"
            }
        }
    }

class CartUpdate(BaseModel):
    """Schema for product updates."""
  
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)

class CheckoutCreate(BaseModel):
    """Schema for checkout creation requests."""
    user_id: int = Field(..., gt=0, description="ID of the user performing the checkout")
    product_id: Optional[int] = Field(None, ge=0, description="ID of the product")
    quantity: int = Field(default=1, gt=0, description="Quantity must be greater than 0")
    price: Decimal = Field(..., ge=0, description="Product price")
    
    @field_validator('user_id')
    @classmethod
    def validate_user_id(cls, v):
        if v is None or v <= 0:
            raise ValueError("user_id must be a positive integer")
        return v
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("quantity must be greater than 0")
        return v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("price cannot be negative")
        return v
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "product_id": 2,
                "quantity": 3,
                "price": 299.99
            }
        }
    }

class CheckoutResponse(BaseModel):
    """Schema for checkout responses."""
  
    checkout_id: Optional[int] = None
    user_id: int
    product_id: Optional[int] = None
    quantity: int
    price: Decimal
    total_price: Decimal
  
    model_config = {
        "json_schema_extra": {
            "example": {
                "checkout_id": 1,
                "user_id": 1,
                "product_id": 2,
                "quantity": 3,
                "price": 299.99,
                "total_price": 899.97
            }
        }
    }

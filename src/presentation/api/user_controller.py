"""User API endpoints and request/response models."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from src.application.dto.user_dto import UserDTO
from src.application.services.user_services import UserService
from src.domain.enums.user_enums import UserStatus
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from src.presentation.api.dependencies import get_user_service


# Pydantic models for API requests/responses
class UserCreate(BaseModel):
    """Schema for user creation requests."""
    
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., max_length=100)  # Would use EmailStr with email-validator package
    status: str = Field(default="active")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "status": "active"
            }
        }


class UserResponse(BaseModel):
    """Schema for user responses."""
    
    id: Optional[int] = None
    username: str
    email: str
    status: str
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "status": "active"
            }
        }


class UserPartialUpdate(BaseModel):
    """Schema for partial user updates."""
    
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = None


# Define the router
router = APIRouter(
    prefix="/api",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


# Convert between DTOs and API models
def _dto_to_response(user_dto: UserDTO) -> UserResponse:
    """Convert a UserDTO to a UserResponse."""
    data = user_dto.to_dict()
    return UserResponse(
        id=data["id"],
        username=data["username"],
        email=data["email"],
        status=data["status"],
    )


def _request_to_dto(user_data: UserCreate, user_id: Optional[int] = None) -> UserDTO:
    """Convert a UserCreate request to a UserDTO."""
    return UserDTO(
        id=user_id,
        username=user_data.username,
        email=user_data.email,
        status=user_data.status,
    )


# Endpoints
@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user with the provided information.
    
    - **username**: unique username for the user
    - **email**: valid email address
    - **status**: user status (active, inactive, pending, banned)
    """
    try:
        user_dto = _request_to_dto(user_data)
        created_user = user_service.create_user(user_dto)
        return _dto_to_response(created_user)
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieve a user by their unique identifier.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    return _dto_to_response(user)


@router.get(
    "/users/by-username/{username}",
    response_model=UserResponse,
    summary="Get user by username",
)
async def get_user_by_username(
    username: str,
    user_service: UserService = Depends(get_user_service),
):
    """
    Retrieve a user by their unique username.
    """
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found",
        )
    return _dto_to_response(user)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Partially update a user",
)
async def update_user_partial(
    user_id: int,
    user_data: UserPartialUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Update specific fields of a user.
    
    - **username**: new username (optional)
    - **email**: new email address (optional)
    - **status**: new status (optional)
    """
    # Extract only non-None fields
    update_data = {
        k: v for k, v in user_data.model_dump().items()
        if v is not None
    }
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update",
        )
    
    updated_user = user_service.update_user_partial(user_id, **update_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    return _dto_to_response(updated_user)


@router.patch(
    "/users/{user_id}/status",
    response_model=UserResponse,
    summary="Update user status",
)
async def update_status(
    user_id: int,
    status_data: dict,
    user_service: UserService = Depends(get_user_service),
):
    """
    Update a user's status.
    
    - **status**: new status value (active, inactive, pending, banned)
    """
    if "status" not in status_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status field is required",
        )
    
    try:
        new_status = status_data["status"]
        # Validate the status
        UserStatus(new_status)
        
        updated_user = user_service.update_user_status(user_id, new_status)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        
        return _dto_to_response(updated_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status: {status_data['status']}. Valid values: {[s.value for s in UserStatus]}",
        )


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    """
    Delete a user by their ID.
    """
    deleted = user_service.delete_user(user_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )


@router.delete(
    "/users/{user_id}/soft",
    response_model=UserResponse,
    summary="Soft delete a user",
)
async def soft_delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    """
    Soft delete a user (mark as inactive).
    """
    updated_user = user_service.soft_delete_user(user_id)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found",
        )
    
    return _dto_to_response(updated_user)

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.category_dto import CategoryDTO
from src.application.services.category_service import CategoryService
from src.domain.exceptions.category_exceptions import CategoryNotFoundError
from src.presentation.api.dependencies import get_category_service
from src.presentation.api.models import CategoryCreate, CategoryResponse, CategoryUpdate


def _dto_to_response(category_dto: CategoryDTO) -> CategoryResponse:
    data = category_dto.to_dict()
    return CategoryResponse(
        category_id=data["category_id"],
        name=data["name"],
        description=data["description"],
    )

def _request_to_dto(category_data: CategoryCreate, category_id: Optional[int] = None) -> CategoryDTO:
    return CategoryDTO(
        category_id=category_id,
        name=category_data.name,
        description=category_data.description,
    )

# Define router
router = APIRouter(
    prefix="/categories",
    tags=["categories"],
    responses={404: {"description": "Category not found"}},
)

@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category",
)

async def create_category(
    category_data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
):
    """Create a new category."""
    try:
        category_dto = _request_to_dto(category_data)
        created_category = category_service.create_category(category_dto)
        return _dto_to_response(created_category)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get category by ID",
)

async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    """Get category by ID."""
    try:
        category = category_service.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError(f"Category with ID {category_id} not found.")
        return _dto_to_response(category)
    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=List[CategoryResponse],
    summary="Get all categories",
)

async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    """Get all categories."""
    categories = category_service.get_all_categories()
    return [_dto_to_response(category) for category in categories]

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update category",
)

async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    """Update an existing category."""
    try:
        category_dto = _request_to_dto(category_data, category_id)
        updated_category = category_service.update_category(category_dto)
        return _dto_to_response(updated_category)
    except CategoryNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
        
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
)

async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
):
    """Delete a category by its ID."""
    deleted = category_service.delete_category(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with ID {category_id} not found",
        )
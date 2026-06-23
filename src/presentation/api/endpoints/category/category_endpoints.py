from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.application.services.category_services import CategoryService
from src.presentation.api.dependencies import get_category_service
from src.presentation.api.models import CategoryCreate, CategoryResponse


router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreate, service: CategoryService = Depends(get_category_service)):
    """Create a new category."""
    try:
        from src.application.dto.category_dto import CategoryDTO
        dto = CategoryDTO(id=None, name=category_data.name, description=category_data.description, status=category_data.status)
        result = service.create_category(dto)
        return CategoryResponse(**result.to_dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[CategoryResponse])
async def list_categories(service: CategoryService = Depends(get_category_service)):
    """Get all categories."""
    categories = service.list_categories()
    return [CategoryResponse(**cat.to_dict()) for cat in categories]


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    """Get category by ID."""
    category = service.get_category_by_id(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return CategoryResponse(**category.to_dict())


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int, service: CategoryService = Depends(get_category_service)):
    """Delete a category."""
    deleted = service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.product_dto import ProductDTO
from src.application.services.product_service import ProductService
from src.domain.exceptions.product_exceptions import ProductNotFoundError
from src.presentation.api.dependencies import get_product_service
from src.presentation.api.models import ProductCreate, ProductResponse, ProductUpdate


def _dto_to_response(product_dto: ProductDTO) -> ProductResponse:
   data = product_dto.to_dict()
   return ProductResponse(
      product_id=data["id"],
      name=data["name"],
      price=data["price"],
      description=data["description"],
   )

def _request_to_dto(product_data: ProductCreate, product_id: Optional[int] = None) -> ProductDTO:
   return ProductDTO(
      product_id=product_id,
      name=product_data.name,
      price=product_data.price,
      description=product_data.description,
   )

# Define router
router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Product not found"}},
)

@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
)
async def create_product(
    product_data: ProductCreate,
    product_service: ProductService = Depends(get_product_service),
):
    """Create a new product."""
    try:
        product_dto = _request_to_dto(product_data)
        created_product = product_service.create_product(product_dto)
        return _dto_to_response(created_product)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID",
)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """Get a product by ID."""
    product = product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )
    return _dto_to_response(product)

@router.get(
    "",
    response_model=List[ProductResponse],
    summary="Get all products",
)
async def get_all_products(
    product_service: ProductService = Depends(get_product_service),
):
    """Get all products."""
    products = product_service.get_all_products()
    return [_dto_to_response(product) for product in products]

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update product",
)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    product_service: ProductService = Depends(get_product_service),
):
    """Update an existing product."""
    try:
        # Get existing product first
        existing_product = product_service.get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found",
            )
      
        # Update only provided fields
        updated_dto = ProductDTO(
            product_id=product_id,
            name=product_data.name if product_data.name else existing_product.name,
            price=product_data.price if product_data.price else existing_product.price,
            description=product_data.description if product_data.description else existing_product.description,
        )
      
        updated_product = product_service.update_product(updated_dto)
        return _dto_to_response(updated_product)
    except ProductNotFoundError as exc:
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
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete product",
)
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """Delete a product by ID."""
    success = product_service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found",
        )


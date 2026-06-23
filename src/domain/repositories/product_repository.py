from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.product import Product
from ..enums.product_enums import ProductStatus
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.services.product_services import ProductService
from src.presentation.api.dependencies import get_product_service
from src.presentation.api.models import ProductCreate, ProductResponse


router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, service: ProductService = Depends(get_product_service)):
    """Create a new product."""
    try:
        from src.application.dto.product_dto import ProductDTO
        dto = ProductDTO(id=None, name=product_data.name, description=product_data.description,
                         price=product_data.price, sku=product_data.sku, status=product_data.status)
        result = service.create_product(dto)
        return ProductResponse(**result.to_dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=List[ProductResponse])
async def list_products(service: ProductService = Depends(get_product_service)):
    """Get all products."""
    products = service.list_products()
    return [ProductResponse(**prod.to_dict()) for prod in products]


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Get product by ID."""
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return ProductResponse(**product.to_dict())


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a product."""
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.checkout_dto import CheckoutDTO
from src.application.services.checkout_service import CheckoutService
from src.domain.exceptions.checkout_exceptions import CheckoutNotFoundError
from src.presentation.api.dependencies import get_checkout_service
from src.presentation.api.models import CheckoutCreate, CheckoutResponse


def _dto_to_response(checkout_dto: CheckoutDTO) -> CheckoutResponse:
    data = checkout_dto.to_dict()
    return CheckoutResponse(
        checkout_id=data["id"],
        user_id=data["user_id"],
        product_id=data["product_id"],
        price=data["price"],
        total_price=data["total_price"],
        quantity=data["quantity"],
    )

def _request_to_dto(checkout_data: CheckoutCreate, checkout_id: Optional[int] = None) -> CheckoutDTO:
    return CheckoutDTO(
        checkout_id=checkout_id,
        user_id=checkout_data.user_id,
        product_id=checkout_data.product_id,
        price=checkout_data.price,
        total_price=checkout_data.price * checkout_data.quantity,
        quantity=checkout_data.quantity,
    )

# Define router
router = APIRouter(
    prefix="/checkouts",
      tags=["checkouts"],
      responses={404: {"description": "Checkout not found"}},
)

@router.post(
    "", 
      response_model=CheckoutResponse,
      status_code=status.HTTP_201_CREATED,
      summary="Create a new checkout",
)
async def create_checkout(
    checkout_data: CheckoutCreate,
    checkout_service: CheckoutService = Depends(get_checkout_service),
):
    """Create a new checkout."""
    try:
        checkout_dto = _request_to_dto(checkout_data)
        created_checkout = checkout_service.create_checkout(checkout_dto)
        return _dto_to_response(created_checkout)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/{checkout_id}",
    response_model=CheckoutResponse,
    summary="Get checkout by ID",
)
async def get_checkout(
    checkout_id: int,
    checkout_service: CheckoutService = Depends(get_checkout_service),
):
    """Get a checkout by ID."""
    try:
        checkout = checkout_service.get_checkout_by_id(checkout_id)
        if checkout is None:
            raise CheckoutNotFoundError(f"Checkout with ID {checkout_id} not found.")
        return _dto_to_response(checkout)
    except CheckoutNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

@router.get(
    "",
    response_model=List[CheckoutResponse],
    summary="Get all checkouts",
)
async def get_all_checkouts(
    checkout_service: CheckoutService = Depends(get_checkout_service),
):
    """Get all checkouts."""
    checkouts = checkout_service.get_all_checkouts()
    return [_dto_to_response(checkout) for checkout in checkouts]

@router.put(
    "/{checkout_id}",
    response_model=CheckoutResponse,
    summary="Update checkout",
)
async def update_checkout(
    checkout_id: int,
    checkout_data: CheckoutCreate,
    checkout_service: CheckoutService = Depends(get_checkout_service),
):
    """Update an existing checkout."""
    try:
        checkout_dto = _request_to_dto(checkout_data, checkout_id)
        updated_checkout = checkout_service.update_checkout(checkout_dto)
        return _dto_to_response(updated_checkout)
    except CheckoutNotFoundError as exc:
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
    "/{checkout_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete checkout",
)
async def delete_checkout(
    checkout_id: int,
    checkout_service: CheckoutService = Depends(get_checkout_service),
):
    """Delete a checkout by ID."""
    deleted = checkout_service.delete_checkout(checkout_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Checkout with ID {checkout_id} not found",
        )

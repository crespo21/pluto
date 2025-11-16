import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status

from src.application.dto.cart_dto import CartDTO
from src.application.services.cart_service import CartService
from src.domain.exceptions.cart_exceptions import CartItemNotFoundError
from src.presentation.api.dependencies import get_cart_service
from src.presentation.api.models import CartAddRequest, CartResponse

logger = logging.getLogger(__name__)

def _dto_to_response(cart_dto: CartDTO) -> CartResponse:
   data = cart_dto.to_dict()
   return CartResponse(
      id=data["id"],
      user_id=data["user_id"],
      product_id=data["product_id"],
      name=data["name"],
      price=data["price"],
      description=data["description"]
   )


def _request_to_dto(cart_data: CartAddRequest, product_id: Optional[int] = None) -> CartDTO:
    return CartDTO(
        id=None,
        user_id=cart_data.user_id,
        product_id=product_id,
        name=cart_data.name,
        price=cart_data.price,
        description=cart_data.description
    )


# Define router
router = APIRouter(
    prefix="/cart",
    tags=["cart"],
    responses={404: {"description": "Cart item not found"}},
)  

@router.post(
    "",
   response_model=CartResponse,
   status_code=status.HTTP_201_CREATED,
   summary="Add item to cart",
)
async def add_to_cart(
    cart_data: CartAddRequest,
    cart_service: CartService = Depends(get_cart_service),
):
    """Add an item to the cart for a specific user."""
    try:
        logger.info(f"Adding item to cart for user {cart_data.user_id}")
        cart_dto = _request_to_dto(cart_data)
        added_item = cart_service.add_to_cart(cart_dto)
        return _dto_to_response(added_item)
    except ValueError as exc:
        logger.error(f"Validation error adding to cart: {str(exc)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

@router.get(
    "/user/{user_id}",
   response_model=List[CartResponse],
   summary="Get all items in cart for a user",
)
async def get_user_cart_items(
    user_id: int,
    cart_service: CartService = Depends(get_cart_service),
):
   """Retrieve all items in the cart for a specific user."""
   try:
      logger.info(f"Fetching cart items for user {user_id}")
      items = cart_service.get_cart_by_user_id(user_id)
      return [_dto_to_response(item) for item in items]
   except Exception as exc:
      logger.error(f"Error fetching cart for user {user_id}: {str(exc)}")
      raise HTTPException(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
         detail="Error retrieving cart items"
      )

@router.get(
    "",
   response_model=List[CartResponse],
   summary="Get all items in cart",
)
async def get_all_cart_items(
    cart_service: CartService = Depends(get_cart_service),
):
   """Retrieve all items in the cart."""
   try:
      logger.info("Fetching all cart items")
      items = cart_service.get_all_products()
      return [_dto_to_response(item) for item in items]
   except Exception as exc:
      logger.error(f"Error fetching all carts: {str(exc)}")
      raise HTTPException(
         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
         detail="Error retrieving cart items"
      )

@router.delete(
    "/{product_id}",
   status_code=status.HTTP_204_NO_CONTENT,
   summary="Remove item from cart",
)
async def remove_from_cart(
    product_id: int,
    cart_service: CartService = Depends(get_cart_service),
):
    """Remove an item from the cart by product ID."""
    try:
        logger.info(f"Removing product {product_id} from cart")
        success = cart_service.delete_cart(product_id)
        if not success:
            logger.warning(f"Product {product_id} not found in cart")
            raise CartItemNotFoundError(f"Cart item with product ID {product_id} not found")
    except CartItemNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
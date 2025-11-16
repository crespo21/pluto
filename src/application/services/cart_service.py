import logging
from typing import Optional, List

from src.application.dto.cart_dto import CartDTO
from src.domain.repositories.cart_repository import CartRepository


class CartService:

   def __init__(self, cart_repository: CartRepository):
      self.cart_repository = cart_repository
      self.logger = logging.getLogger(__name__)

   def add_to_cart(self, cart_dto: CartDTO) -> CartDTO:
      try:
         self.logger.info(f"Adding item to cart for user {cart_dto.user_id}")
         cart_entity = cart_dto.to_domain()
         created_cart = self.cart_repository.add_to_cart(cart_entity)
         self.logger.info(f"Successfully added item to cart: {created_cart.id}")
         return CartDTO.from_domain(created_cart)
      except Exception as e:
         self.logger.error(f"Error adding to cart: {str(e)}")
         raise

   def get_product_by_id(self, product_id: int) -> Optional[CartDTO]:
      """Get product by ID."""
      try:
         self.logger.debug(f"Fetching product {product_id} from cart")
         cart = self.cart_repository.find_by_product_id(product_id)
         return CartDTO.from_domain(cart) if cart else None
      except Exception as e:
         self.logger.error(f"Error fetching product {product_id}: {str(e)}")
         raise

   def get_all_products(self) -> List[CartDTO]:
      """Get all products."""
      try:
         self.logger.info("Fetching all cart items")
         cart = self.cart_repository.find_all()
         return [CartDTO.from_domain(product) for product in cart]
      except Exception as e:
         self.logger.error(f"Error fetching all products: {str(e)}")
         raise

   def get_cart_by_user_id(self, user_id: int) -> List[CartDTO]:
      """Get all cart items for a specific user."""
      try:
         self.logger.info(f"Fetching cart items for user {user_id}")
         carts = self.cart_repository.get_by_user_id(user_id)
         self.logger.info(f"Found {len(carts)} items in cart for user {user_id}")
         return [CartDTO.from_domain(cart) for cart in carts]
      except Exception as e:
         self.logger.error(f"Error fetching cart for user {user_id}: {str(e)}")
         raise

   def delete_cart(self, product_id: int) -> bool:
      """Delete product by ID."""
      try:
         self.logger.info(f"Removing product {product_id} from cart")
         result = self.cart_repository.remove_from_cart(product_id)
         self.logger.info(f"Successfully removed product {product_id}" if result else f"Product {product_id} not found")
         return result
      except Exception as e:
         self.logger.error(f"Error deleting product {product_id}: {str(e)}")
         raise
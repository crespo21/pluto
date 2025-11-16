import logging
from typing import Optional, List

from decimal import Decimal
from src.domain.entities.checkout import Checkout
from src.domain.enums.checkout_enums import CheckoutStatus
         

from src.application.dto.checkout_dto import CheckoutDTO
from src.application.dto.cart_dto import CartDTO
from src.domain.repositories.checkout_repository import CheckoutRepository

class CheckoutService:
   """Application service for Checkout use cases."""

   def __init__(self, checkout_repository: CheckoutRepository):
      self.checkout_repository = checkout_repository
      self.logger = logging.getLogger(__name__)

   def create_checkout(self, checkout_dto: CheckoutDTO) -> CheckoutDTO:
      """Create a new checkout."""
      try:
         self.logger.info(f"Creating checkout for user {checkout_dto.user_id}")
         checkout_entity = checkout_dto.to_domain()
         created_checkout = self.checkout_repository.create(checkout_entity)
         self.logger.info(f"Checkout {created_checkout.checkout_id} created successfully")
         return CheckoutDTO.from_domain(created_checkout)
      except Exception as e:
         self.logger.error(f"Error creating checkout: {str(e)}")
         raise

   def create_checkout_from_cart(self, user_id: int, cart_dto: CartDTO, quantity: int = 1) -> CheckoutDTO:
      """Create a checkout from a cart item."""
      try:
         self.logger.info(f"Creating checkout from cart for user {user_id}, product {cart_dto.product_id}")
         checkout = Checkout(
            user_id=user_id,
            product_id=cart_dto.product_id,
            quantity=quantity,
            price=cart_dto.price,
            status=CheckoutStatus.PENDING
         )
         created_checkout = self.checkout_repository.create(checkout)
         self.logger.info(f"Checkout created from cart: {created_checkout.checkout_id}")
         return CheckoutDTO.from_domain(created_checkout)
      except Exception as e:
         self.logger.error(f"Error creating checkout from cart: {str(e)}")
         raise

   def get_checkout_by_id(self, checkout_id: int) -> Optional[CheckoutDTO]:
      """Get checkout by ID."""
      try:
         self.logger.debug(f"Fetching checkout {checkout_id}")
         checkout = self.checkout_repository.find_by_id(checkout_id)
         return CheckoutDTO.from_domain(checkout) if checkout else None
      except Exception as e:
         self.logger.error(f"Error fetching checkout {checkout_id}: {str(e)}")
         raise

   def get_all_checkouts(self) -> List[CheckoutDTO]:
      """Get all checkouts."""
      try:
         self.logger.info("Fetching all checkouts")
         checkouts = self.checkout_repository.find_all()
         self.logger.info(f"Found {len(checkouts)} checkouts")
         return [CheckoutDTO.from_domain(checkout) for checkout in checkouts]
      except Exception as e:
         self.logger.error(f"Error fetching all checkouts: {str(e)}")
         raise

   def get_checkouts_by_user(self, user_id: int) -> List[CheckoutDTO]:
      """Get all checkouts for a specific user."""
      try:
         self.logger.info(f"Fetching checkouts for user {user_id}")
         checkouts = self.checkout_repository.find_by_user_id(user_id)
         self.logger.info(f"Found {len(checkouts)} checkouts for user {user_id}")
         return [CheckoutDTO.from_domain(checkout) for checkout in checkouts]
      except Exception as e:
         self.logger.error(f"Error fetching checkouts for user {user_id}: {str(e)}")
         raise

   def update_checkout(self, checkout_dto: CheckoutDTO) -> CheckoutDTO:
      """Update existing checkout."""
      try:
         self.logger.info(f"Updating checkout {checkout_dto.checkout_id}")
         checkout_entity = checkout_dto.to_domain()
         updated_checkout = self.checkout_repository.update(checkout_entity)
         self.logger.info(f"Checkout {checkout_dto.checkout_id} updated successfully")
         return CheckoutDTO.from_domain(updated_checkout)
      except Exception as e:
         self.logger.error(f"Error updating checkout {checkout_dto.checkout_id}: {str(e)}")
         raise

   def delete_checkout(self, checkout_id: int) -> bool:
      """Delete checkout by ID."""
      try:
         self.logger.info(f"Deleting checkout {checkout_id}")
         result = self.checkout_repository.delete_by_id(checkout_id)
         self.logger.info(f"Checkout {checkout_id} deleted" if result else f"Checkout {checkout_id} not found")
         return result
      except Exception as e:
         self.logger.error(f"Error deleting checkout {checkout_id}: {str(e)}")
         raise
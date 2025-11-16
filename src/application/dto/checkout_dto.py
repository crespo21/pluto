from dataclasses import dataclass
from typing import Optional
from decimal import Decimal
from datetime import datetime

from src.domain.entities.checkout import Checkout

@dataclass(frozen=True)
class CheckoutDTO:
   """Application-layer representation of a checkout."""

   checkout_id: Optional[int]
   user_id: int
   product_id: Optional[int]
   quantity: int
   price: Decimal
   total_price: Decimal
   


   def to_domain(self) -> Checkout:
      """Convert DTO to domain entity."""
      return Checkout(
         checkout_id=self.checkout_id,
         user_id=self.user_id,
         product_id=self.product_id,
         quantity=self.quantity,
         price=self.price,
         total_price=self.total_price,
      )

   def to_dict(self) -> dict:
      """Serialize DTO to dictionary."""
      return {
         "id": self.checkout_id,
         "user_id": self.user_id,
         "product_id": self.product_id,
         "quantity": self.quantity,
         "price": float(self.price),
         "total_price": float(self.total_price),
      }

   @classmethod
   def from_domain(cls, checkout: Checkout) -> "CheckoutDTO":
      """Create DTO from domain entity."""
      return cls(
         checkout_id=checkout.checkout_id,
         user_id=checkout.user_id,
         product_id=checkout.product_id,
         quantity=checkout.quantity,
         price=checkout.price,
         total_price=checkout.total_price,
      )

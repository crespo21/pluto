from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from src.domain.entities.cart import Cart

@dataclass(frozen=True)
class CartDTO:

   id: Optional[int]
   user_id: int
   product_id: Optional[int]
   name: str
   price: Decimal
   description: str

   def to_domain(self) -> Cart:
      return Cart(
         user_id=self.user_id,
         product_id=self.product_id,
         name=self.name,
         price=self.price,
         description=self.description
      )
   
   def to_dict(self) -> dict:
      return {
         "id": self.id,
         "user_id": self.user_id,
         "product_id": self.product_id,
         "name": self.name,
         "price": float(self.price),
         "description": self.description,
      }
   
   @classmethod
   def from_domain(cls, cart: Cart) -> "CartDTO":
      """Create DTO from domain entity."""
      return cls(
         id=cart.id,
         user_id=cart.user_id,
         product_id=cart.product_id,
         name=cart.name,
         price=cart.price,
         description=cart.description,
      )
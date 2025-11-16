from typing import Optional
from decimal import Decimal


class Cart:

   def __init__(self, user_id: int, product_id: Optional[int], name: str, price: Decimal, description: str, id: Optional[int] = None):
      if user_id is None or user_id <= 0:
         raise ValueError("user_id is required and must be positive")
      if not name or len(name.strip()) == 0:
         raise ValueError("name cannot be empty")
      if price < 0:
         raise ValueError("price cannot be negative")

      self.id = id
      self.user_id = user_id
      self.product_id = product_id
      self.name = name
      self.price = price
      self.description = description

   def __repr__(self):
      return f"Cart(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, name={self.name})"
   
   

   def to_dict(self):
      return {
         "id": self.id,
         "user_id": self.user_id,
         "product_id": self.product_id,
         "name": self.name,
         "price": float(self.price),
         "description": self.description
      }
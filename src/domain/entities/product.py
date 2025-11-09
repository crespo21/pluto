from typing import Optional
from decimal import Decimal

class Product:

   def __init__(self, product_id: Optional[int], name: str, price: Decimal, description: str):

      self.product_id = product_id
      self.name = name
      self.price = price
      self.description = description

   def __repr__(self):
      return f"Product(id={self.product_id}, name={self.name}, price={self.price}, description={self.description})"

   def update_price(self, new_price: Decimal):
      if new_price <= 0:
         raise ValueError("Price must be positive")
      self.price = new_price

   def to_dict(self):
      return {
         "product_id": self.product_id,
         "name": self.name,
         "price": float(self.price),
         "description": self.description
      }






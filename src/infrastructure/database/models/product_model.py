from decimal import Decimal
from typing import Any
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from .user_model import Base
from src.domain.entities.product import Product

class ProductModel(Base):
   __tablename__ = "products"

   product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   name: Mapped[str] = mapped_column(String(100), nullable=False)
   price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
   description: Mapped[str] = mapped_column(String(255), nullable=True)

   def __repr__(self) -> str:
      return f"ProductModel(id={self.product_id}, name={self.name}, price={self.price}, description={self.description})"
   
   def to_domain(self) -> Product:
      return Product(
         product_id=self.product_id,
         name=self.name,
         price=self.price,
         description=self.description
      )
   
   @classmethod
   def from_domain(cls, product: Product) -> "ProductModel":
      kwargs: dict[str, Any] = {
         "name": product.name,
         "price": product.price,
         "description": product.description
      }

      if product.product_id is not None:
         kwargs["product_id"] = product.product_id
      return cls(**kwargs)
   

 
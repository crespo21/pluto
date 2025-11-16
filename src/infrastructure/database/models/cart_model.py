from decimal import Decimal
from typing import Any
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .user_model import Base
from src.domain.entities.cart import Cart


class CartModel(Base):
   __tablename__ = "cart"

   id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
   product_id: Mapped[int] = mapped_column(nullable=True)
   name: Mapped[str] = mapped_column(String(100), nullable=False)
   price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
   description: Mapped[str] = mapped_column(String(255), nullable=True)

   def __repr__(self) -> str:
      return f"CartModel(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, name={self.name})"
   
   def to_domain(self) -> Cart:
      return Cart(
         id=self.id,
         user_id=self.user_id,
         product_id=self.product_id,
         name=self.name,
         price=self.price,
         description=self.description
      )
   
   @classmethod
   def from_domain(cls, cart: Cart) -> "CartModel":
      kwargs: dict[str, Any] = {
         "user_id": cart.user_id,
         "name": cart.name,
         "price": cart.price,
         "description": cart.description
      }

      if cart.id is not None:
         kwargs["id"] = cart.id
      if cart.product_id is not None:
         kwargs["product_id"] = cart.product_id
      return cls(**kwargs)
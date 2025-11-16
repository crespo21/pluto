from decimal import Decimal
from typing import Any, Optional
from sqlalchemy import String, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column
from .user_model import Base
from src.domain.entities.checkout import Checkout

class CheckoutModel(Base):
   __tablename__ = "checkouts"

   checkout_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
   user_id: Mapped[int] = mapped_column(nullable=False)
   product_id: Mapped[Optional[int]] = mapped_column(nullable=True)
   quantity: Mapped[int] = mapped_column(nullable=False, default=1)
   price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
   total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
   status: Mapped[str] = mapped_column(Enum("pending", "completed", "cancelled", "failed", name="checkout_status"), nullable=False, default="pending")
   # created_at: Mapped[Any] = mapped_column(nullable=False)
   # updated_at: Mapped[Any] = mapped_column(nullable=False)

   def __repr__(self) -> str:
      return (f"CheckoutModel(id={self.checkout_id}, user_id={self.user_id}, "
               f"product_id={self.product_id}, quantity={self.quantity}, "
               f"price={self.price}, total_price={self.total_price}, "
               f"status={self.status}, ")

   def to_domain(self) -> Checkout:
      return Checkout(
         checkout_id=self.checkout_id,
         user_id=self.user_id,
         product_id=self.product_id,
         quantity=self.quantity,
         price=self.price,
         total_price=self.total_price,
         # created_at=self.created_at,
         # updated_at=self.updated_at
      )

   @classmethod
   def from_domain(cls, checkout: Checkout) -> "CheckoutModel":
      kwargs: dict[str, Any] = {
         "user_id": checkout.user_id,
         "product_id": checkout.product_id,
         "quantity": checkout.quantity,
         "price": checkout.price,
         "total_price": checkout.total_price,
         "status": checkout.status.value,
         # "created_at": checkout.created_at,
         # "updated_at": checkout.updated_at
      }

      if checkout.checkout_id is not None:
         kwargs["checkout_id"] = checkout.checkout_id
      return cls(**kwargs)
   
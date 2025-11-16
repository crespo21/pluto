import logging 
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.repositories.cart_repository import CartRepository
from src.domain.entities.cart import Cart
from src.domain.exceptions.cart_exceptions import CartItemNotFoundError
from ..models.cart_model import CartModel


class SqlAlchemyCartRepository(CartRepository):

   def __init__(self, session: Session):
      self.session = session
      self.logger = logging.getLogger(__name__)

   def add_to_cart(self, cart: Cart) -> Cart:
      try:
         cart_model = CartModel.from_domain(cart)
         self.session.add(cart_model)
         self.session.commit()
         self.session.refresh(cart_model)
         self.logger.info(f"Added cart item for user {cart.user_id}")
         return cart_model.to_domain()
      except IntegrityError as e:
         self.session.rollback()
         self.logger.error(f"Integrity error while adding to cart: {str(e)}")
         raise ValueError("Invalid cart data: user or constraint violation")
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while adding to cart: {str(e)}")
         raise

   def find_by_product_id(self, product_id: int) -> Optional[Cart]:
      try:
         cart_model = self.session.get(CartModel, product_id)
         return cart_model.to_domain() if cart_model else None
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while finding cart: {str(e)}")
         raise

   def find_all(self) -> List[Cart]:
      try:
         results = self.session.execute(select(CartModel)).scalars().all()
         return [model.to_domain() for model in results]
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while fetching all carts: {str(e)}")
         raise

   def remove_from_cart(self, product_id: int) -> bool:
      try:
         cart_model = self.session.get(CartModel, product_id)
         if not cart_model:
            self.logger.warning(f"Cart item {product_id} not found for deletion")
            return False

         self.session.delete(cart_model)
         self.session.commit()
         self.logger.info(f"Removed cart item {product_id}")
         return True
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while removing from cart: {str(e)}")
         raise

   def clear_cart(self) -> None:
      try:
         self.session.query(CartModel).delete()
         self.session.commit()
         self.logger.info("Cleared all cart items")
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while clearing cart: {str(e)}")
         raise

   def get_total_price(self) -> float:
      try:
         total: Decimal = self.session.query(
            func.coalesce(func.sum(CartModel.price), 0)
         ).scalar()
         return float(total)
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while calculating total price: {str(e)}")
         raise

   def find_by_user_id(self, user_id: int) -> List[Cart]:
      try:
         results = self.session.execute(
            select(CartModel).where(CartModel.user_id == user_id)
         ).scalars().all()
         self.logger.info(f"Found {len(results)} cart items for user {user_id}")
         return [model.to_domain() for model in results]
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while fetching cart for user {user_id}: {str(e)}")
         raise

   def find_by_user_id_and_product_id(self, user_id: int, product_id: int) -> Optional[Cart]:
      try:
         cart_model = self.session.execute(
            select(CartModel).where(
               (CartModel.user_id == user_id) & (CartModel.product_id == product_id)
            )
         ).scalar_one_or_none()
         return cart_model.to_domain() if cart_model else None
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while finding cart for user {user_id}, product {product_id}: {str(e)}")
         raise
   
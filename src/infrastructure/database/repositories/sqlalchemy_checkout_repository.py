import logging 
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.repositories.checkout_repository import CheckoutRepository
from src.domain.entities.checkout import Checkout
from src.domain.exceptions.checkout_exceptions import CheckoutNotFoundError
from ..models.checkout_model import CheckoutModel

class SqlAlchemyCheckoutRepository(CheckoutRepository):

   def __init__(self, session: Session):
      self.session = session
      self.logger = logging.getLogger(__name__)

   def create(self, checkout: Checkout) -> Checkout:
      try:
         checkout_model = CheckoutModel.from_domain(checkout)
         self.session.add(checkout_model)
         self.session.commit()
         self.session.refresh(checkout_model)
         self.logger.info(f"Created checkout for user {checkout.user_id}")
         return checkout_model.to_domain()
      except IntegrityError as e:
         self.session.rollback()
         self.logger.error(f"Integrity error while creating checkout: {str(e)}")
         raise ValueError("Invalid checkout data: constraint violation")
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while creating checkout: {str(e)}")
         raise

   def find_by_id(self, checkout_id: int) -> Optional[Checkout]:
      try:
         checkout_model = self.session.get(CheckoutModel, checkout_id)
         return checkout_model.to_domain() if checkout_model else None
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while finding checkout {checkout_id}: {str(e)}")
         raise

   def find_all(self) -> List[Checkout]:
      try:
         results = self.session.execute(select(CheckoutModel)).scalars().all()
         return [model.to_domain() for model in results]
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while fetching all checkouts: {str(e)}")
         raise

   def find_by_user_id(self, user_id: int) -> List[Checkout]:
      try:
         results = self.session.execute(
            select(CheckoutModel).where(CheckoutModel.user_id == user_id)
         ).scalars().all()
         self.logger.info(f"Found {len(results)} checkouts for user {user_id}")
         return [model.to_domain() for model in results]
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while fetching checkouts for user {user_id}: {str(e)}")
         raise

   def find_by_user_id_and_product_id(self, user_id: int, product_id: int) -> Optional[Checkout]:
      try:
         checkout_model = self.session.execute(
            select(CheckoutModel).where(
               (CheckoutModel.user_id == user_id) & 
               (CheckoutModel.product_id == product_id)
            )
         ).scalar_one_or_none()
         return checkout_model.to_domain() if checkout_model else None
      except SQLAlchemyError as e:
         self.logger.error(f"Database error while finding checkout for user {user_id}, product {product_id}: {str(e)}")
         raise

   def update(self, checkout: Checkout) -> Checkout:
      try:
         if checkout.checkout_id is None:
            raise ValueError("Checkout ID is required for update")
         
         checkout_model = self.session.get(CheckoutModel, checkout.checkout_id)
         if not checkout_model:
            self.logger.warning(f"Checkout {checkout.checkout_id} not found for update")
            raise CheckoutNotFoundError(f"Checkout with ID {checkout.checkout_id} not found")
         
         checkout_model.user_id = checkout.user_id
         checkout_model.product_id = checkout.product_id
         checkout_model.quantity = checkout.quantity
         checkout_model.price = checkout.price
         checkout_model.total_price = checkout.total_price
         checkout_model.status = checkout.status.value

         self.session.commit()
         self.session.refresh(checkout_model)
         self.logger.info(f"Updated checkout {checkout.checkout_id}")
         return checkout_model.to_domain()
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while updating checkout {checkout.checkout_id}: {str(e)}")
         raise

   def delete_by_id(self, checkout_id: int) -> bool:
      try:
         checkout_model = self.session.get(CheckoutModel, checkout_id)
         if not checkout_model:
            self.logger.warning(f"Checkout {checkout_id} not found for deletion")
            return False

         self.session.delete(checkout_model)
         self.session.commit()
         self.logger.info(f"Deleted checkout {checkout_id}")
         return True
      except SQLAlchemyError as e:
         self.session.rollback()
         self.logger.error(f"Database error while deleting checkout {checkout_id}: {str(e)}")
         raise
   
   
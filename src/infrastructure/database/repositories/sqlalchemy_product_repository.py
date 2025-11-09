import logging
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import select

from src.domain.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.domain.exceptions.product_exceptions import ProductNotFoundError
from ..models.product_model import ProductModel

class SqlAlchemyProductRepository(ProductRepository):

   def __init__(self, session: Session):
      self.session = session
      self.logger = logging.getLogger(__name__)

   def create(self, product: Product) -> Product:
      product_model = ProductModel.from_domain(product)
      try:
         self.session.add(product_model)
         self.session.commit()
         self.session.refresh(product_model)
      except:
         self.session.rollback()
         raise

      return product_model.to_domain()

   def find_by_id(self, product_id: int) -> Optional[Product]:
      product_model = self.session.get(ProductModel, product_id)
      return product_model.to_domain() if product_model else None

   def find_all(self) -> List[Product]:
      results = self.session.execute(select(ProductModel)).scalars().all()
      return [model.to_domain() for model in results]

   def update(self, product: Product) -> Product:
      if product.product_id is None:
         raise ValueError("Product ID is required for update")
      
      product_model = self.session.get(ProductModel, product.product_id)
      if not product_model:
         raise ProductNotFoundError(f"Product with ID {product.product_id} not found")
      
      product_model.name = product.name
      product_model.price = product.price
      product_model.description = product.description

      self.session.commit()
      self.session.refresh(product_model)

      return product_model.to_domain()

   def delete_by_id(self, product_id: int) -> bool:
      product_model = self.session.get(ProductModel, product_id)
      if not product_model:
         return False

      self.session.delete(product_model)
      self.session.commit()
      return True
     
   
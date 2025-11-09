from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.product import Product

class ProductRepository(ABC):

   @abstractmethod
   def create(self, product: Product) -> Product:
      pass

   @abstractmethod
   def find_by_id(self, product_id: int) -> Optional[Product]:
      pass

   @abstractmethod
   def find_all(self) -> List[Product]:
      pass

   @abstractmethod
   def update(self, product: Product) -> Product:
      pass

   @abstractmethod
   def delete_by_id(self, product_id: int) -> bool:
      pass





from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.category import Category


class CategoryRepository(ABC):

   @abstractmethod
   def create(self, category: Category) -> Category:
      pass

   @abstractmethod
   def find_by_id(self, category_id: int) -> Optional[Category]:
      pass

   @abstractmethod
   def find_all(self) -> List[Category]:
      pass

   @abstractmethod
   def update(self, category: Category) -> Category:
      pass

   @abstractmethod
   def delete_by_id(self, category_id: int) -> bool:
      pass

   
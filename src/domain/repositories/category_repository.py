from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.category import Category
from ..enums.category_enums import CategoryStatus


class CategoryRepository(ABC):
    @abstractmethod
    def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    def find_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Category]:
        pass

    @abstractmethod
    def find_all(self, limit: Optional[int] = None) -> List[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete_by_id(self, category_id: int) -> bool:
        pass
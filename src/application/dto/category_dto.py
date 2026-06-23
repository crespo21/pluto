from dataclasses import dataclass
from typing import Optional, Union
from src.domain.entities.category import Category
from src.domain.enums.category_enums import CategoryStatus


@dataclass(frozen=True)
class CategoryDTO:
    id: Optional[int]
    name: str
    description: Optional[str]
    status: Union[str, CategoryStatus]

    def to_domain(self) -> Category:
        status_value = self.status if isinstance(self.status, CategoryStatus) else CategoryStatus(self.status)
        return Category(
            category_id=self.id,
            name=self.name,
            description=self.description,
            status=status_value
        )

    def to_dict(self) -> dict:
        status_value = self.status.value if isinstance(self.status, CategoryStatus) else self.status
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": status_value
        }

    @classmethod
    def from_domain(cls, category: Category) -> "CategoryDTO":
        return cls(
            id=category.category_id,
            name=category.category_name,
            description=category.category_description,
            status=category.category_status
        )
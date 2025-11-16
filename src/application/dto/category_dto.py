from dataclasses import dataclass
from typing import Optional
from src.domain.entities.category import Category

@dataclass(frozen=True)
class CategoryDTO:
    """Application-layer representation of a category."""
    
    category_id: Optional[int]
    name: str
    description: str

    def to_domain(self) -> Category:
        """Convert DTO to domain entity."""
        return Category(
            category_id=self.category_id,
            name=self.name,
            description=self.description,
        )

    def to_dict(self) -> dict:
        """Serialize DTO to dictionary."""
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def from_domain(cls, category: Category) -> "CategoryDTO":
        """Create DTO from domain entity."""
        return cls(
            category_id=category.category_id,
            name=category.name,
            description=category.description,
        )
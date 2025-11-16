from typing import Optional
from sqlalchemy import Column, Integer, String  
from sqlalchemy.ext.declarative import declarative_base
from decimal import Decimal
from src.domain.entities.category import Category
from src.infrastructure.database.models.user_model import Base
from typing import Any
from sqlalchemy.orm import Mapped, mapped_column


class CategoryModel(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"CategoryModel(id={self.category_id}, name={self.name}, description={self.description})"
    
    def to_domain(self) -> Category:
        return Category(
            category_id=self.category_id,
            name=self.name,
            description=self.description
        )
    
    @classmethod
    def from_domain(cls, category: Category) -> "CategoryModel":
        kwargs: dict[str, Any] = {
            "name": category.name,
            "description": category.description
        }

        if category.category_id is not None:
            kwargs["category_id"] = category.category_id
        return cls(**kwargs)
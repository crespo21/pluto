from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.category import Category
from src.domain.enums.category_enums import CategoryStatus
from .user_model import Base


class CategoryModel(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")

    def __repr__(self) -> str:
        return f"CategoryModel(id={self.id}, name='{self.name}', status='{self.status}')"

    def to_domain(self) -> Category:
        return Category(
            category_id=self.id,
            name=self.name,
            description=self.description,
            status=CategoryStatus(self.status)
        )

    @classmethod
    def from_domain(cls, category: Category) -> "CategoryModel":
        status_value = category.category_status.value if isinstance(category.category_status, CategoryStatus) else category.category_status
        return cls(
            id=category.category_id if category.category_id else None,
            name=category.category_name,
            description=category.category_description,
            status=status_value
        )
import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from src.domain.repositories.category_repository import CategoryRepository
from src.domain.entities.category import Category
from src.domain.enums.category_enums import CategoryStatus
from ..models.category_model import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _model_to_domain(category_model: CategoryModel) -> Category:
        return category_model.to_domain()

    def create(self, category: Category) -> Category:
        category_model = CategoryModel.from_domain(category)
        self.session.add(category_model)
        self.session.commit()
        self.session.refresh(category_model)
        return self._model_to_domain(category_model)

    def find_by_id(self, category_id: int) -> Optional[Category]:
        category_model = self.session.get(CategoryModel, category_id)
        return self._model_to_domain(category_model) if category_model else None

    def find_by_name(self, name: str) -> Optional[Category]:
        category_model = self.session.execute(
            select(CategoryModel).where(CategoryModel.name == name)
        ).scalar_one_or_none()
        return self._model_to_domain(category_model) if category_model else None

    def find_all(self, limit: Optional[int] = None) -> List[Category]:
        query = select(CategoryModel)
        if limit:
            query = query.limit(limit)
        results = self.session.execute(query).scalars().all()
        return [self._model_to_domain(model) for model in results]

    def update(self, category: Category) -> Category:
        if category.category_id is None:
            raise ValueError("Category ID required for update")
        category_model = self.session.get(CategoryModel, category.category_id)
        if not category_model:
            raise ValueError(f"Category {category.category_id} not found")
        category_model.name = category.category_name
        category_model.status = category.category_status.value
        self.session.commit()
        self.session.refresh(category_model)
        return self._model_to_domain(category_model)

    def delete_by_id(self, category_id: int) -> bool:
        category_model = self.session.get(CategoryModel, category_id)
        if not category_model:
            return False
        self.session.delete(category_model)
        self.session.commit()
        return True
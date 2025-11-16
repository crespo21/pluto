import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.domain.repositories.category_repository import CategoryRepository
from src.domain.entities.category import Category
from src.domain.exceptions.category_exceptions import CategoryNotFoundError
from ..models.category_model import CategoryModel


class SqlAlchemyCategoryRepository(CategoryRepository):

    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    def create(self, category: Category) -> Category:
        category_model = CategoryModel.from_domain(category)
        try:
            self.session.add(category_model)
            self.session.commit()
            self.session.refresh(category_model)
        except:
            self.session.rollback()
            raise

        return category_model.to_domain()

    def find_by_id(self, category_id: int) -> Optional[Category]:
        category_model = self.session.get(CategoryModel, category_id)
        return category_model.to_domain() if category_model else None

    def find_all(self) -> List[Category]:
        results = self.session.execute(select(CategoryModel)).scalars().all()
        return [model.to_domain() for model in results]

    def update(self, category: Category) -> Category:
        if category.category_id is None:
            raise ValueError("Category ID is required for update")
        
        category_model = self.session.get(CategoryModel, category.category_id)
        if not category_model:
            raise CategoryNotFoundError(f"Category with ID {category.category_id} not found")
        
        category_model.name = category.name
        category_model.description = category.description

        self.session.commit()
        self.session.refresh(category_model)

        return category_model.to_domain()

    def delete_by_id(self, category_id: int) -> bool:
        category_model = self.session.get(CategoryModel, category_id)
        if not category_model:
            return False

        self.session.delete(category_model)
        self.session.commit()
        return True
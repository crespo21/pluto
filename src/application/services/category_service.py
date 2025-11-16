from typing import List, Optional
from src.application.dto.category_dto import CategoryDTO
from src.domain.repositories.category_repository import CategoryRepository


class CategoryService:
    """Application service for Category use cases."""

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def create_category(self, category_dto: CategoryDTO) -> CategoryDTO:
        """Create a new category."""
        category_entity = category_dto.to_domain()
        created_category = self.category_repository.create(category_entity)
        return CategoryDTO.from_domain(created_category)

    def get_category_by_id(self, category_id: int) -> Optional[CategoryDTO]:
        """Get category by ID."""
        category = self.category_repository.find_by_id(category_id)
        return CategoryDTO.from_domain(category) if category else None

    def get_all_categories(self) -> List[CategoryDTO]:
        """Get all categories."""
        categories = self.category_repository.find_all()
        return [CategoryDTO.from_domain(category) for category in categories]

    def update_category(self, category_dto: CategoryDTO) -> CategoryDTO:
        """Update existing category."""
        category_entity = category_dto.to_domain()
        updated_category = self.category_repository.update(category_entity)
        return CategoryDTO.from_domain(updated_category)

    def delete_category(self, category_id: int) -> bool:
        """Delete category by ID."""
        return self.category_repository.delete_by_id(category_id)
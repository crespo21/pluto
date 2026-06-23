from typing import Optional, List
from src.application.dto.category_dto import CategoryDTO
from src.domain.repositories.category_repository import CategoryRepository


class CategoryService:
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

    def get_category_by_name(self, name: str) -> Optional[CategoryDTO]:
        """Get category by name."""
        category = self.category_repository.find_by_name(name)
        return CategoryDTO.from_domain(category) if category else None

    def list_categories(self) -> List[CategoryDTO]:
        """List all categories."""
        categories = self.category_repository.find_all()
        return [CategoryDTO.from_domain(cat) for cat in categories]

    def delete_category(self, category_id: int) -> bool:
        """Delete a category."""
        return self.category_repository.delete_by_id(category_id)
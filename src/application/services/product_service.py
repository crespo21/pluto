from typing import Optional, List

from src.application.dto.product_dto import ProductDTO
from src.domain.repositories.product_repository import ProductRepository

class ProductService:
    """Application service for Product use cases."""
  
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Create a new product."""
        product_entity = product_dto.to_domain()
        created_product = self.product_repository.create(product_entity)
        return ProductDTO.from_domain(created_product)

    def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """Get product by ID."""
        product = self.product_repository.find_by_id(product_id)
        return ProductDTO.from_domain(product) if product else None

    def get_all_products(self) -> List[ProductDTO]:
        """Get all products."""
        products = self.product_repository.find_all()
        return [ProductDTO.from_domain(product) for product in products]

    def update_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Update existing product."""
        product_entity = product_dto.to_domain()
        updated_product = self.product_repository.update(product_entity)
        return ProductDTO.from_domain(updated_product)

    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID."""
        return self.product_repository.delete_by_id(product_id)

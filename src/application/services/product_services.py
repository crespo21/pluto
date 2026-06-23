from typing import Optional, List
from src.application.dto.product_dto import ProductDTO
from src.domain.repositories.product_repository import ProductRepository


class ProductService:
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

    def get_product_by_sku(self, sku: str) -> Optional[ProductDTO]:
        """Get product by SKU."""
        product = self.product_repository.find_by_sku(sku)
        return ProductDTO.from_domain(product) if product else None

    def list_products(self) -> List[ProductDTO]:
        """List all products."""
        products = self.product_repository.find_all()
        return [ProductDTO.from_domain(prod) for prod in products]

    def update_product_price(self, product_id: int, new_price: float) -> Optional[ProductDTO]:
        """Update product price."""
        product = self.product_repository.find_by_id(product_id)
        if product:
            product.product_price = new_price
            updated = self.product_repository.update(product)
            return ProductDTO.from_domain(updated) if updated else None
        return None

    def delete_product(self, product_id: int) -> bool:
        """Delete a product."""
        return self.product_repository.delete_by_id(product_id)
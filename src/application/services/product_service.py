import logging
from typing import Optional, List

from src.application.dto.product_dto import ProductDTO
from src.domain.repositories.product_repository import ProductRepository

class ProductService:
    """Application service for Product use cases."""
  
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
        self.logger = logging.getLogger(__name__)

    def create_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Create a new product."""
        try:
            self.logger.info(f"Creating product: {product_dto.name}")
            product_entity = product_dto.to_domain()
            created_product = self.product_repository.create(product_entity)
            self.logger.info(f"Product {created_product.product_id} created successfully")
            return ProductDTO.from_domain(created_product)
        except Exception as e:
            self.logger.error(f"Error creating product: {str(e)}")
            raise

    def get_product_by_id(self, product_id: int) -> Optional[ProductDTO]:
        """Get product by ID."""
        try:
            self.logger.debug(f"Fetching product {product_id}")
            product = self.product_repository.find_by_id(product_id)
            return ProductDTO.from_domain(product) if product else None
        except Exception as e:
            self.logger.error(f"Error fetching product {product_id}: {str(e)}")
            raise

    def get_all_products(self) -> List[ProductDTO]:
        """Get all products."""
        try:
            self.logger.info("Fetching all products")
            products = self.product_repository.find_all()
            self.logger.info(f"Found {len(products)} products")
            return [ProductDTO.from_domain(product) for product in products]
        except Exception as e:
            self.logger.error(f"Error fetching all products: {str(e)}")
            raise

    def update_product(self, product_dto: ProductDTO) -> ProductDTO:
        """Update existing product."""
        try:
            self.logger.info(f"Updating product {product_dto.product_id}")
            product_entity = product_dto.to_domain()
            updated_product = self.product_repository.update(product_entity)
            self.logger.info(f"Product {product_dto.product_id} updated successfully")
            return ProductDTO.from_domain(updated_product)
        except Exception as e:
            self.logger.error(f"Error updating product {product_dto.product_id}: {str(e)}")
            raise

    def delete_product(self, product_id: int) -> bool:
        """Delete product by ID."""
        try:
            self.logger.info(f"Deleting product {product_id}")
            result = self.product_repository.delete_by_id(product_id)
            self.logger.info(f"Product {product_id} deleted" if result else f"Product {product_id} not found")
            return result
        except Exception as e:
            self.logger.error(f"Error deleting product {product_id}: {str(e)}")
            raise


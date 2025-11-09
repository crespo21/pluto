from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

from src.domain.entities.product import Product

@dataclass(frozen=True)
class ProductDTO:
    """Application-layer representation of a product."""
  
    product_id: Optional[int]
    name: str
    price: Decimal
    description: str

    def to_domain(self) -> Product:
        """Convert DTO to domain entity."""
        return Product(
            product_id=self.product_id,
            name=self.name,
            price=self.price,
            description=self.description,
        )

    def to_dict(self) -> dict:
        """Serialize DTO to dictionary."""
        return {
            "id": self.product_id,
            "name": self.name,
            "price": float(self.price),
            "description": self.description,
        }

    @classmethod
    def from_domain(cls, product: Product) -> "ProductDTO":
        """Create DTO from domain entity."""
        return cls(
            product_id=product.product_id,
            name=product.name,
            price=product.price,
            description=product.description,
        )
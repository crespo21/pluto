from dataclasses import dataclass
from typing import Optional, Union
from src.domain.entities.product import Product
from src.domain.enums.product_enums import ProductStatus


@dataclass(frozen=True)
class ProductDTO:
    id: Optional[int]
    name: str
    description: Optional[str]
    price: float
    sku: str
    status: Union[str, ProductStatus]

    def to_domain(self) -> Product:
        status_value = self.status if isinstance(self.status, ProductStatus) else ProductStatus(self.status)
        return Product(
            product_id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            sku=self.sku,
            status=status_value
        )

    def to_dict(self) -> dict:
        status_value = self.status.value if isinstance(self.status, ProductStatus) else self.status
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "sku": self.sku,
            "status": status_value
        }

    @classmethod
    def from_domain(cls, product: Product) -> "ProductDTO":
        return cls(
            id=product.product_id,
            name=product.product_name,
            description=product.product_description,
            price=product.product_price,
            sku=product.product_sku,
            status=product.product_status
        )
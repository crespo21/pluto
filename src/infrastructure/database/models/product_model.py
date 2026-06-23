from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.product import Product
from src.domain.enums.product_enums import ProductStatus
from .user_model import Base


class ProductModel(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=True)

    def __repr__(self) -> str:
        return f"ProductModel(id={self.id}, name='{self.name}', price={self.price}, status='{self.status}')"

    def to_domain(self) -> Product:
        return Product(
            product_id=self.id,
            name=self.name,
            description=self.description,
            price=self.price,
            sku=self.sku,
            status=ProductStatus(self.status)
        )

    @classmethod
    def from_domain(cls, product: Product) -> "ProductModel":
        status_value = product.product_status.value if isinstance(product.product_status, ProductStatus) else product.product_status
        return cls(
            id=product.product_id if product.product_id else None,
            name=product.product_name,
            description=product.product_description,
            price=product.product_price,
            sku=product.product_sku,
            status=status_value
        )
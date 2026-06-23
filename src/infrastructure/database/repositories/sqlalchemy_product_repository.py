import logging
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from src.domain.repositories.product_repository import ProductRepository
from src.domain.entities.product import Product
from src.domain.enums.product_enums import ProductStatus
from ..models.product_model import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _model_to_domain(product_model: ProductModel) -> Product:
        return product_model.to_domain()

    def create(self, product: Product) -> Product:
        product_model = ProductModel.from_domain(product)
        self.session.add(product_model)
        self.session.commit()
        self.session.refresh(product_model)
        return self._model_to_domain(product_model)

    def find_by_id(self, product_id: int) -> Optional[Product]:
        product_model = self.session.get(ProductModel, product_id)
        return self._model_to_domain(product_model) if product_model else None

    def find_by_sku(self, sku: str) -> Optional[Product]:
        product_model = self.session.execute(
            select(ProductModel).where(ProductModel.sku == sku)
        ).scalar_one_or_none()
        return self._model_to_domain(product_model) if product_model else None

    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Product]:
        query = select(ProductModel)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        results = self.session.execute(query).scalars().all()
        return [self._model_to_domain(model) for model in results]

    def find_by_status(self, status: ProductStatus) -> List[Product]:
        results = self.session.execute(
            select(ProductModel).where(ProductModel.status == status.value)
        ).scalars().all()
        return [self._model_to_domain(model) for model in results]

    def update(self, product: Product) -> Product:
        if product.product_id is None:
            raise ValueError("Product ID required for update")
        product_model = self.session.get(ProductModel, product.product_id)
        if not product_model:
            raise ValueError(f"Product {product.product_id} not found")
        product_model.name = product.product_name
        product_model.price = product.product_price
        product_model.status = product.product_status.value
        self.session.commit()
        self.session.refresh(product_model)
        return self._model_to_domain(product_model)

    def delete_by_id(self, product_id: int) -> bool:
        product_model = self.session.get(ProductModel, product_id)
        if not product_model:
            return False
        self.session.delete(product_model)
        self.session.commit()
        return True
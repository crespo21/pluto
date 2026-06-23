from src.domain.enums.product_enums import ProductStatus


class Product:
    def __init__(self, product_id, name, description, price, sku, status):
        self.product_id = product_id
        self.product_name = name
        self.product_description = description
        self.product_price = price
        self.product_sku = sku
        self.product_status = status

    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.product_name}', price={self.product_price}, status={self.product_status})"

    def update_price(self, new_price: float):
        self.product_price = new_price

    def update_status(self, new_status: ProductStatus):
        self.product_status = new_status

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_description": self.product_description,
            "product_price": self.product_price,
            "product_sku": self.product_sku,
            "status": self.product_status.value if isinstance(self.product_status, ProductStatus) else self.product_status
        }
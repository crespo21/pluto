from src.domain.enums.category_enums import CategoryStatus


class Category:
    def __init__(self, category_id, name, description, status):
        self.category_id = category_id
        self.category_name = name
        self.category_description = description
        self.category_status = status

    def __repr__(self):
        return f"Category(id={self.category_id}, name='{self.category_name}', status={self.category_status})"

    def update_status(self, new_status: CategoryStatus):
        self.category_status = new_status

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "category_description": self.category_description,
            "status": self.category_status.value if isinstance(self.category_status, CategoryStatus) else self.category_status
        }
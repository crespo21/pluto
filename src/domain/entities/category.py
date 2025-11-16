from typing import Optional

class Category:
   def __init__(self, category_id: Optional[int], name: str, description: str):
      self.category_id = category_id
      self.name = name
      self.description = description

   def __repr__(self):
      return f"Category(id={self.category_id}, name={self.name}, description={self.description})"
   
   def to_dict(self):
      return {
         "category_id": self.category_id,
         "name": self.name,
         "description": self.description
      }
   
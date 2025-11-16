from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.cart import Cart

class CartRepository(ABC):

   @abstractmethod
   def add_to_cart(self, cart: Cart) -> Cart:
      pass

   @abstractmethod
   def find_by_product_id(self, product_id: int) -> Optional[Cart]:
      pass

   @abstractmethod
   def find_all(self) -> List[Cart]:
      pass

   @abstractmethod
   def remove_from_cart(self, product_id: int) -> bool:
      pass

   @abstractmethod
   def clear_cart(self) -> None:
      pass

   # @abstractmethod
   # def update_cart(self) -> None:
   #    pass

   @abstractmethod
   def get_total_price(self) -> float:
      pass
   
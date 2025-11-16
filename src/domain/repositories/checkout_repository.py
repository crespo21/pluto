from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.checkout import Checkout

class CheckoutRepository(ABC):

    @abstractmethod
    def create(self, checkout: Checkout) -> Checkout:
        pass

    @abstractmethod
    def find_by_id(self, checkout_id: int) -> Optional[Checkout]:
        pass

    @abstractmethod
    def find_all(self) -> List[Checkout]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Checkout]:
        pass

    @abstractmethod
    def find_by_user_id_and_product_id(self, user_id: int, product_id: int) -> Optional[Checkout]:
        pass

    @abstractmethod
    def update(self, checkout: Checkout) -> Checkout:
        pass

    @abstractmethod
    def delete_by_id(self, checkout_id: int) -> bool:
        pass
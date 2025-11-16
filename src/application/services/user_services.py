from typing import Optional, Union, List
from decimal import Decimal

from src.application.dto.user_dto import UserDTO
from src.application.dto.cart_dto import CartDTO
from src.application.dto.checkout_dto import CheckoutDTO
from src.domain.enums.user_enums import UserStatus
from src.domain.enums.checkout_enums import CheckoutStatus
from src.domain.repositories.user_repository import UserRepository
from src.application.services.cart_service import CartService
from src.application.services.checkout_service import CheckoutService

class UserService:
    def __init__(self, user_repository: UserRepository, cart_service: Optional[CartService] = None, checkout_service: Optional[CheckoutService] = None):
        self.user_repository = user_repository
        self.cart_service = cart_service
        self.checkout_service = checkout_service

    def create_user(self, user_dto: UserDTO) -> UserDTO:
        user_entity = user_dto.to_domain()
        created_user = self.user_repository.create(user_entity)
        created_user_dto = UserDTO.from_domain(created_user)
        
        return created_user_dto
    
    def bulk_create_users(self, user_dtos: list[UserDTO]) -> list[UserDTO]:
        user_entities = [dto.to_domain() for dto in user_dtos]
        created_users = self.user_repository.bulk_create(user_entities)
        return [UserDTO.from_domain(user) for user in created_users]

    def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        user = self.user_repository.find_by_id(user_id)
        return UserDTO.from_domain(user) if user else None

    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        user = self.user_repository.find_by_username(username)
        return UserDTO.from_domain(user) if user else None

    def update_user_status(self, user_id: int, user_status: Union[str, UserStatus]) -> Optional[UserDTO]:
        user = self.user_repository.find_by_id(user_id)
        if user:
            status_enum = user_status if isinstance(user_status, UserStatus) else UserStatus(user_status)
            user.update_status(status_enum)
            updated_user = self.user_repository.update_status(user_id, status_enum)
            return UserDTO.from_domain(updated_user) if updated_user else None
        return None
    
    def delete_user(self, user_id: int) -> bool:
        return self.user_repository.delete_by_id(user_id)
    
    def soft_delete_user(self, user_id: int) -> Optional[UserDTO]:
        user = self.user_repository.soft_delete(user_id)
        return UserDTO.from_domain(user) if user else None
    
    def bulk_delete_users(self, user_ids: list[int]) -> int:
        return self.user_repository.bulk_delete(user_ids)
    
    def update_user_partial(self, user_id: int, **kwargs) -> Optional[UserDTO]:
        user = self.user_repository.update_partial(user_id, **kwargs)
        return UserDTO.from_domain(user) if user else None
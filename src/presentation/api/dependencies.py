"""FastAPI dependency injection functions for services and repositories."""
from src.application.services.product_service import ProductService
from src.domain.repositories.product_repository import ProductRepository
from src.infrastructure.database.repositories.sqlalchemy_product_repository import SqlAlchemyProductRepository

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.services.user_services import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.config import get_session
from src.infrastructure.database.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository

from src.application.services.category_service import CategoryService
from src.domain.repositories.category_repository import CategoryRepository
from src.infrastructure.database.repositories.sqlalchemy_category_repository import SqlAlchemyCategoryRepository

from src.application.services.cart_service import CartService
from src.domain.repositories.cart_repository import CartRepository
from src.infrastructure.database.repositories.sqlalchemy_cart_repository import SqlAlchemyCartRepository    

from src.application.services.checkout_service import CheckoutService
from src.domain.repositories.checkout_repository import CheckoutRepository
from src.infrastructure.database.repositories.sqlalchemy_checkout_repository import SqlAlchemyCheckoutRepository

def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Provide a UserRepository instance with injected session."""
    return SqlAlchemyUserRepository(session=session)

def get_product_repository(session: Session = Depends(get_session)) -> ProductRepository:
    """Provide a ProductRepository instance with injected session."""
    return SqlAlchemyProductRepository(session=session)

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    """Provide a ProductService instance with injected repository."""
    return ProductService(product_repository=repo)

def get_category_repository(session: Session = Depends(get_session)) -> CategoryRepository:
    """Provide a CategoryRepository instance with injected session."""
    return SqlAlchemyCategoryRepository(session=session)

def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    """Provide a CategoryService instance with injected repository."""
    return CategoryService(category_repository=repo)

def get_cart_repository(session: Session = Depends(get_session)) -> CartRepository:
    return SqlAlchemyCartRepository(session=session)

def get_cart_service(repo: CartRepository = Depends(get_cart_repository)) -> CartService:
    """Provide a CategoryService instance with injected repository."""
    return CartService(cart_repository=repo)

def get_checkout_repository(session: Session = Depends(get_session)) -> CheckoutRepository:
    return SqlAlchemyCheckoutRepository(session=session)

def get_checkout_service(repo: CheckoutRepository = Depends(get_checkout_repository)) -> CheckoutService:
    """Provide a CheckoutService instance with injected repository."""
    return CheckoutService(checkout_repository=repo)

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    cart_service: CartService = Depends(get_cart_service),
    checkout_service: CheckoutService = Depends(get_checkout_service)
) -> UserService:
    """Provide a UserService instance with injected repository and services."""
    return UserService(user_repository=repo, cart_service=cart_service, checkout_service=checkout_service)
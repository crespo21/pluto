"""FastAPI dependency injection functions for services and repositories."""

from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.services.user_services import UserService
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.config import get_session
from src.infrastructure.database.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    """Provide a UserRepository instance with injected session."""
    return SqlAlchemyUserRepository(session=session)


def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    """Provide a UserService instance with injected repository."""
    return UserService(user_repository=repo)
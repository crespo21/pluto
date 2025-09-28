import logging
from sqlalchemy.orm import Session
from typing import Iterable, List, Optional
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from src.domain.enums.user_enums import UserStatus
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from ..models.user_model import UserModel

class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
        self.logger = logging.getLogger(__name__)

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    @staticmethod
    def _ensure_status(status: UserStatus | str) -> UserStatus:
        return status if isinstance(status, UserStatus) else UserStatus(status)

    @staticmethod
    def _model_to_domain(user_model: UserModel) -> User:
        return user_model.to_domain()

    def _persist(self) -> None:
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def _refresh(self, models: Iterable[UserModel]) -> None:
        for model in models:
            self.session.refresh(model)

    # --------------------------------------------------------
    # Create operations
    # --------------------------------------------------------
    def create(self, user: User) -> User:
        if self.exists_by_username(user.user_name) or self.exists_by_email(user.user_email):
            error_msg = f"User already exists with username '{user.user_name}' or email '{user.user_email}'"
            self.logger.warning(error_msg)
            raise UserAlreadyExistsError(error_msg)

        user_model = UserModel.from_domain(user)

        try:
            self.session.add(user_model)
            self._persist()
            self.session.refresh(user_model)
        except IntegrityError as exc:
            self.logger.error("Integrity error while creating user: %s", exc)
            self.session.rollback()
            raise UserAlreadyExistsError(str(exc)) from exc
        except Exception:
            self.logger.exception("Unexpected error while creating user")
            self.session.rollback()
            raise

        return self._model_to_domain(user_model)

    def bulk_create(self, users: List[User]) -> List[User]:
        user_models = [UserModel.from_domain(user) for user in users]

        try:
            self.session.add_all(user_models)
            self._persist()
            self._refresh(user_models)
        except IntegrityError as exc:
            self.logger.error("Integrity error during bulk create: %s", exc)
            self.session.rollback()
            raise UserAlreadyExistsError(str(exc)) from exc
        except Exception:
            self.logger.exception("Unexpected error during bulk create")
            self.session.rollback()
            raise

        return [self._model_to_domain(model) for model in user_models]

    # --------------------------------------------------------
    # Read operations
    # --------------------------------------------------------
    def find_by_id(self, user_id: int) -> Optional[User]:
        user_model = self.session.get(UserModel, user_id)
        return self._model_to_domain(user_model) if user_model else None

    def find_by_username(self, username: str) -> Optional[User]:
        user_model = (
            self.session.execute(
                select(UserModel).where(UserModel.username == username)
            ).scalar_one_or_none()
        )
        return self._model_to_domain(user_model) if user_model else None

    def find_by_email(self, email: str) -> Optional[User]:
        user_model = (
            self.session.execute(
                select(UserModel).where(UserModel.email == email)
            ).scalar_one_or_none()
        )
        return self._model_to_domain(user_model) if user_model else None

    def find_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[User]:
        query = select(UserModel)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        results = self.session.execute(query).scalars().all()
        return [self._model_to_domain(model) for model in results]

    def find_by_status(self, status: UserStatus | str, limit: Optional[int] = None) -> List[User]:
        status_enum = self._ensure_status(status)
        query = select(UserModel).where(UserModel.status == status_enum.value)
        if limit is not None:
            query = query.limit(limit)

        results = self.session.execute(query).scalars().all()
        return [self._model_to_domain(model) for model in results]

    def count_total(self) -> int:
        return self.session.execute(select(func.count()).select_from(UserModel)).scalar_one()

    def exists_by_username(self, username: str) -> bool:
        return (
            self.session.execute(
                select(UserModel.id).where(UserModel.username == username)
            ).first()
            is not None
        )

    def exists_by_email(self, email: str) -> bool:
        return (
            self.session.execute(
                select(UserModel.id).where(UserModel.email == email)
            ).first()
            is not None
        )

    # --------------------------------------------------------
    # Update operations
    # --------------------------------------------------------
    def update(self, user: User) -> User:
        if user.user_id is None:
            raise ValueError("User ID is required for update operations")

        user_model = self.session.get(UserModel, user.user_id)
        if not user_model:
            raise ValueError(f"User with id {user.user_id} not found")

        user_model.username = user.user_name
        user_model.email = user.user_email
        user_model.status = self._ensure_status(user.user_status).value

        self._persist()
        self.session.refresh(user_model)
        return self._model_to_domain(user_model)

    def update_partial(self, user_id: int, **kwargs) -> Optional[User]:
        user_model = self.session.get(UserModel, user_id)
        if not user_model:
            return None

        if "username" in kwargs:
            user_model.username = kwargs["username"]
        if "email" in kwargs:
            user_model.email = kwargs["email"]
        if "status" in kwargs:
            user_model.status = self._ensure_status(kwargs["status"]).value

        self._persist()
        self.session.refresh(user_model)

        return self._model_to_domain(user_model)

    def update_status(self, user_id: int, status: UserStatus | str) -> Optional[User]:
        user_model = self.session.get(UserModel, user_id)
        if not user_model:
            return None

        user_model.status = self._ensure_status(status).value
        self._persist()
        self.session.refresh(user_model)

        return self._model_to_domain(user_model)

    # --------------------------------------------------------
    # Delete operations
    # --------------------------------------------------------
    def delete_by_id(self, user_id: int) -> bool:
        user_model = self.session.get(UserModel, user_id)
        if not user_model:
            return False

        self.session.delete(user_model)
        self._persist()
        return True

    def delete_by_username(self, username: str) -> bool:
        user_model = (
            self.session.execute(
                select(UserModel).where(UserModel.username == username)
            ).scalar_one_or_none()
        )
        if not user_model:
            return False

        self.session.delete(user_model)
        self._persist()
        return True

    def soft_delete(self, user_id: int) -> Optional[User]:
        return self.update_status(user_id, UserStatus.INACTIVE)

    def bulk_delete(self, user_ids: List[int]) -> int:
        if not user_ids:
            return 0

        deleted = (
            self.session.query(UserModel)
            .filter(UserModel.id.in_(user_ids))
            .delete(synchronize_session=False)
        )
        self._persist()
        return deleted

    def delete_all(self) -> int:
        deleted = self.session.query(UserModel).delete(synchronize_session=False)
        self._persist()
        return deleted

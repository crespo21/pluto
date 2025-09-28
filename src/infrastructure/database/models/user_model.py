from typing import Any

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"UserModel(id={self.id}, username='{self.username}', email='{self.email}', status='{self.status}')"

    def to_domain(self) -> User:
        status_value = UserStatus(self.status)
        return User(
            user_id=self.id,
            username=self.username,
            email=self.email,
            status=status_value,
        )

    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        status_value = user.user_status.value
        if isinstance(user.user_status, UserStatus):
            status_value = user.user_status.value
        else:
            status_value = UserStatus(user.user_status).value

        kwargs: dict[str, Any] = {
            "username": user.user_name,
            "email": user.user_email,
            "status": status_value,
        }

        if user.user_id is not None:
            kwargs["id"] = user.user_id

        return cls(**kwargs)

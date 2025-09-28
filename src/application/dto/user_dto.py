from dataclasses import dataclass
from typing import Optional, Union

from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus


@dataclass(frozen=True)
class UserDTO:
    """Application-layer representation of a user used for inbound/outbound data."""

    id: Optional[int]
    username: str
    email: str
    status: Union[str, UserStatus]

    def to_domain(self) -> User:
        """Convert the DTO into a domain entity."""
        status_value = self.status

        if isinstance(status_value, UserStatus):
            status_enum = status_value
        else:
            try:
                status_enum = UserStatus(status_value)
            except ValueError as exc:
                raise ValueError(f"Unsupported user status: {status_value}") from exc

        return User(
            user_id=self.id,
            username=self.username,
            email=self.email,
            status=status_enum,
        )

    def to_dict(self) -> dict:
        """Serialize the DTO into a JSON-friendly dictionary."""
        status_value = self.status.value if isinstance(self.status, UserStatus) else self.status

        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "status": status_value,
        }

    @classmethod
    def from_domain(cls, user: User) -> "UserDTO":
        """Create a DTO from a domain entity."""
        status_value = user.user_status
        if isinstance(status_value, UserStatus):
            status_label = status_value
        else:
            status_label = UserStatus(status_value)

        return cls(
            id=user.user_id,
            username=user.user_name,
            email=user.user_email,
            status=status_label,
        )
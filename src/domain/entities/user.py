from typing import Optional

from src.domain.enums.user_enums import UserStatus

class User:
    def __init__(self, user_id: Optional[int], username: str, email: str, status: UserStatus):
        self.user_id = user_id
        self.user_name = username
        self.user_email = email
        self.user_status = status

    def __repr__(self):
        return f"User(user_id={self.user_id}, user_name='{self.user_name}', user_email='{self.user_email}', user_status={self.user_status})"

    def deactivate(self):
        self.user_status = UserStatus.INACTIVE

    def update_email(self, new_email: str):
        self.user_email = new_email

    def update_username(self, new_username: str):
        self.user_name = new_username

    def update_status(self, new_status: UserStatus):
        self.user_status = new_status

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "status": self.user_status.value if isinstance(self.user_status, UserStatus) else self.user_status
        }
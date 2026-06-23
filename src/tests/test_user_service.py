# @"
# """Unit tests for UserService."""
import pytest
from unittest.mock import Mock

from src.application.dto.user_dto import UserDTO
from src.application.services.user_services import UserService
from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def user_service(mock_repository):
    return UserService(user_repository=mock_repository)


class TestUserServiceCreate:
    """Tests for user creation."""

    def test_create_user_success(self, user_service, mock_repository):
        user_dto = UserDTO(id=None, username="testuser", email="test@example.com", status="active")
        created_user = User(user_id=1, username="testuser", email="test@example.com", status=UserStatus.ACTIVE)
        mock_repository.create.return_value = created_user

        result = user_service.create_user(user_dto)

        assert result.id == 1
        assert result.username == "testuser"
        mock_repository.create.assert_called_once()

    def test_create_user_already_exists(self, user_service, mock_repository):
        user_dto = UserDTO(id=None, username="existing", email="existing@example.com", status="active")
        mock_repository.create.side_effect = UserAlreadyExistsError("User exists")

        with pytest.raises(UserAlreadyExistsError):
            user_service.create_user(user_dto)


class TestUserServiceRead:
    """Tests for reading users."""

    def test_get_user_by_id_found(self, user_service, mock_repository):
        user = User(user_id=1, username="testuser", email="test@example.com", status=UserStatus.ACTIVE)
        mock_repository.find_by_id.return_value = user

        result = user_service.get_user_by_id(1)

        assert result is not None
        assert result.id == 1
        assert result.username == "testuser"

    def test_get_user_by_id_not_found(self, user_service, mock_repository):
        mock_repository.find_by_id.return_value = None
        result = user_service.get_user_by_id(999)
        assert result is None

    def test_get_user_by_username(self, user_service, mock_repository):
        user = User(user_id=1, username="testuser", email="test@example.com", status=UserStatus.ACTIVE)
        mock_repository.find_by_username.return_value = user

        result = user_service.get_user_by_username("testuser")

        assert result is not None
        assert result.username == "testuser"


class TestUserServiceUpdate:
    """Tests for updating users."""

    def test_update_user_status(self, user_service, mock_repository):
        updated_user = User(user_id=1, username="testuser", email="test@example.com", status=UserStatus.INACTIVE)
        mock_repository.update_status.return_value = updated_user

        result = user_service.update_user_status(1, "inactive")

        assert result.status == UserStatus.INACTIVE
        mock_repository.update_status.assert_called_once()

    def test_update_user_partial(self, user_service, mock_repository):
        updated_user = User(user_id=1, username="newname", email="test@example.com", status=UserStatus.ACTIVE)
        mock_repository.update_partial.return_value = updated_user

        result = user_service.update_user_partial(1, username="newname")

        assert result.username == "newname"


class TestUserServiceDelete:
    """Tests for deleting users."""

    def test_delete_user_success(self, user_service, mock_repository):
        mock_repository.delete_by_id.return_value = True
        result = user_service.delete_user(1)
        assert result is True

    def test_delete_user_not_found(self, user_service, mock_repository):
        mock_repository.delete_by_id.return_value = False
        result = user_service.delete_user(999)
        assert result is False

    def test_soft_delete_user(self, user_service, mock_repository):
        inactive_user = User(user_id=1, username="testuser", email="test@example.com", status=UserStatus.INACTIVE)
        mock_repository.soft_delete.return_value = inactive_user

        result = user_service.soft_delete_user(1)

        assert result.status == UserStatus.INACTIVE
# "@ | Out-File -Encoding UTF8 "src\tests\test_user_service.py"
# Write-Host "✓ Created test_user_service.py"
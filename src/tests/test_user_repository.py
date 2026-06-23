"""Integration tests for UserRepository."""
import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities.user import User
from src.domain.enums.user_enums import UserStatus
from src.domain.exceptions.user_exceptions import UserAlreadyExistsError
from src.infrastructure.database.models.user_model import Base
from src.infrastructure.database.repositories.sqlalchemy_user_repository import SqlAlchemyUserRepository


@pytest.fixture(scope="function")
def test_db():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def repository(test_db):
    """Create repository with test database."""
    return SqlAlchemyUserRepository(session=test_db)


class TestUserRepositoryCreate:
    """Tests for user creation."""

    def test_create_user(self, repository):
        user = User(user_id=None, username="alice", email="alice@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        assert created.user_id is not None
        assert created.user_name == "alice"
        assert created.user_email == "alice@example.com"

    def test_create_user_duplicate_username(self, repository):
        user1 = User(user_id=None, username="bob", email="bob@example.com", status=UserStatus.ACTIVE)
        repository.create(user1)

        user2 = User(user_id=None, username="bob", email="bob2@example.com", status=UserStatus.ACTIVE)
        with pytest.raises(UserAlreadyExistsError):
            repository.create(user2)

    def test_bulk_create(self, repository):
        users = [
            User(user_id=None, username="user1", email="user1@example.com", status=UserStatus.ACTIVE),
            User(user_id=None, username="user2", email="user2@example.com", status=UserStatus.ACTIVE),
        ]
        created = repository.bulk_create(users)

        assert len(created) == 2
        assert all(u.user_id is not None for u in created)


class TestUserRepositoryRead:
    """Tests for reading users."""

    def test_find_by_id(self, repository):
        user = User(user_id=None, username="charlie", email="charlie@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        found = repository.find_by_id(created.user_id)

        assert found is not None
        assert found.user_name == "charlie"

    def test_find_by_username(self, repository):
        user = User(user_id=None, username="dave", email="dave@example.com", status=UserStatus.ACTIVE)
        repository.create(user)

        found = repository.find_by_username("dave")

        assert found is not None
        assert found.user_email == "dave@example.com"

    def test_find_by_status(self, repository):
        user1 = User(user_id=None, username="eve", email="eve@example.com", status=UserStatus.ACTIVE)
        user2 = User(user_id=None, username="frank", email="frank@example.com", status=UserStatus.INACTIVE)
        repository.create(user1)
        repository.create(user2)

        active = repository.find_by_status(UserStatus.ACTIVE)

        assert len(active) == 1
        assert active[0].user_name == "eve"


class TestUserRepositoryUpdate:
    """Tests for updating users."""

    def test_update_status(self, repository):
        user = User(user_id=None, username="grace", email="grace@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        updated = repository.update_status(created.user_id, UserStatus.INACTIVE)

        assert updated.user_status == UserStatus.INACTIVE

    def test_update_partial(self, repository):
        user = User(user_id=None, username="hank", email="hank@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        updated = repository.update_partial(created.user_id, username="hank_updated")

        assert updated.user_name == "hank_updated"


class TestUserRepositoryDelete:
    """Tests for deleting users."""

    def test_delete_by_id(self, repository):
        user = User(user_id=None, username="iris", email="iris@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        deleted = repository.delete_by_id(created.user_id)

        assert deleted is True
        assert repository.find_by_id(created.user_id) is None

    def test_soft_delete(self, repository):
        user = User(user_id=None, username="jack", email="jack@example.com", status=UserStatus.ACTIVE)
        created = repository.create(user)

        soft_deleted = repository.soft_delete(created.user_id)

        assert soft_deleted.user_status == UserStatus.INACTIVE

from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from auth.exceptions import UserAlreadyExistsError
from auth.hashers.password_hasher import PasswordHasher
from auth.models import User
from auth.repositories.user_repository import UserRepository
from auth.services.user_service import UserService

PASSWORD = "correct-horse"
PASSWORD_HASH = "hashed-correct-horse"


@pytest.fixture
def repository(mocker: MockerFixture) -> MagicMock:
    mock: MagicMock = mocker.create_autospec(UserRepository, instance=True)
    mock.get.return_value = None
    return mock


@pytest.fixture
def hasher(mocker: MockerFixture) -> MagicMock:
    mock: MagicMock = mocker.create_autospec(PasswordHasher, instance=True)
    mock.hash.return_value = PASSWORD_HASH
    return mock


@pytest.fixture
def service(repository: MagicMock, hasher: MagicMock) -> UserService:
    return UserService(repository=repository, hasher=hasher)


def test_register_stores_user_with_hashed_password(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    user = service.register("alice", PASSWORD)

    assert user == User(username="alice", password_hash=PASSWORD_HASH)
    hasher.hash.assert_called_once_with(PASSWORD)
    repository.add.assert_called_once_with(user)


def test_register_rejects_a_taken_username(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = User(username="alice", password_hash="existing")

    with pytest.raises(UserAlreadyExistsError) as exc_info:
        service.register("alice", PASSWORD)

    assert exc_info.value.username == "alice"
    repository.add.assert_not_called()
    hasher.hash.assert_not_called()

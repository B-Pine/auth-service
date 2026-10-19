import logging
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from auth.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.hashers.password_hasher import PasswordHasher
from auth.models import User
from auth.repositories.user_repository import UserRepository
from auth.services.user_service import UserService

PASSWORD = "correct-horse"
PASSWORD_HASH = "hashed-correct-horse"
ALICE = User(username="alice", password_hash=PASSWORD_HASH)


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


@pytest.mark.parametrize("password", ["", "short", "7-chars"])
def test_register_rejects_a_password_shorter_than_8_characters(
    service: UserService, repository: MagicMock, hasher: MagicMock, password: str
) -> None:
    with pytest.raises(InvalidPasswordError, match="at least 8 characters"):
        service.register("alice", password)

    repository.add.assert_not_called()
    hasher.hash.assert_not_called()


def test_register_accepts_a_password_of_exactly_8_characters(
    service: UserService, repository: MagicMock
) -> None:
    service.register("alice", "8-chars!")

    repository.add.assert_called_once()


def test_password_policy_is_checked_before_the_username(
    service: UserService, repository: MagicMock
) -> None:
    repository.get.return_value = User(username="alice", password_hash="existing")

    with pytest.raises(InvalidPasswordError):
        service.register("alice", "short")


def test_login_with_unknown_username_raises_user_not_found(
    service: UserService,
) -> None:
    with pytest.raises(UserNotFoundError) as exc_info:
        service.login("bob", PASSWORD)

    assert exc_info.value.username == "bob"


def test_login_with_correct_password_returns_the_user(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = True

    user = service.login("alice", PASSWORD)

    assert user == ALICE
    hasher.verify.assert_called_once_with(PASSWORD, PASSWORD_HASH)


def test_login_with_wrong_password_raises_invalid_password(
    service: UserService, repository: MagicMock, hasher: MagicMock
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = False

    with pytest.raises(InvalidPasswordError, match="Incorrect password"):
        service.login("alice", "wrong-password")


def test_registration_is_logged(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        service.register("alice", PASSWORD)

    assert "user registered username=alice" in caplog.text


def test_weak_password_registration_is_logged_as_warning(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO), pytest.raises(InvalidPasswordError):
        service.register("alice", "short")

    assert "WARNING" in caplog.text
    assert "registration rejected username=alice reason=weak_password" in caplog.text


def test_taken_username_registration_is_logged_as_warning(
    service: UserService, repository: MagicMock, caplog: pytest.LogCaptureFixture
) -> None:
    repository.get.return_value = ALICE

    with caplog.at_level(logging.INFO), pytest.raises(UserAlreadyExistsError):
        service.register("alice", PASSWORD)

    assert "WARNING" in caplog.text
    assert "registration rejected username=alice reason=username_taken" in caplog.text


def test_successful_login_is_logged(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = True

    with caplog.at_level(logging.INFO):
        service.login("alice", PASSWORD)

    assert "login succeeded username=alice" in caplog.text


def test_login_with_unknown_username_is_logged_as_warning(
    service: UserService, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO), pytest.raises(UserNotFoundError):
        service.login("bob", PASSWORD)

    assert "WARNING" in caplog.text
    assert "login failed username=bob reason=unknown_user" in caplog.text


def test_login_with_wrong_password_is_logged_as_warning(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    repository.get.return_value = ALICE
    hasher.verify.return_value = False

    with caplog.at_level(logging.INFO), pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-password")

    assert "WARNING" in caplog.text
    assert "login failed username=alice reason=wrong_password" in caplog.text


def test_passwords_and_hashes_never_appear_in_logs(
    service: UserService,
    repository: MagicMock,
    hasher: MagicMock,
    caplog: pytest.LogCaptureFixture,
) -> None:
    with caplog.at_level(logging.DEBUG):
        service.register("alice", PASSWORD)
        repository.get.return_value = ALICE
        hasher.verify.return_value = False
        with pytest.raises(InvalidPasswordError):
            service.login("alice", "wrong-secret")

    assert PASSWORD not in caplog.text
    assert "wrong-secret" not in caplog.text
    assert PASSWORD_HASH not in caplog.text

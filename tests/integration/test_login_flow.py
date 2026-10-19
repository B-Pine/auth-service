import pytest

from auth.exceptions import InvalidPasswordError, UserNotFoundError
from auth.hashers.bcrypt_password_hasher import BcryptPasswordHasher
from auth.repositories.in_memory_user_repository import InMemoryUserRepository
from auth.services.user_service import UserService


@pytest.fixture
def service() -> UserService:
    service = UserService(
        repository=InMemoryUserRepository(), hasher=BcryptPasswordHasher(rounds=4)
    )
    service.register("alice", "correct-horse")
    return service


def test_registered_user_can_log_in(service: UserService) -> None:
    assert service.login("alice", "correct-horse").username == "alice"


def test_wrong_password_is_rejected(service: UserService) -> None:
    with pytest.raises(InvalidPasswordError):
        service.login("alice", "wrong-password")


def test_unknown_user_is_rejected(service: UserService) -> None:
    with pytest.raises(UserNotFoundError):
        service.login("bob", "correct-horse")

import pytest

from auth.exceptions import InvalidPasswordError
from auth.hashers.bcrypt_password_hasher import BcryptPasswordHasher
from auth.repositories.in_memory_user_repository import InMemoryUserRepository
from auth.services.user_service import UserService


def test_registered_password_is_stored_as_a_verifiable_hash() -> None:
    repository = InMemoryUserRepository()
    hasher = BcryptPasswordHasher(rounds=4)
    service = UserService(repository=repository, hasher=hasher)

    service.register("alice", "correct-horse")

    stored = repository.get("alice")
    assert stored is not None
    assert stored.password_hash != "correct-horse"
    assert hasher.verify("correct-horse", stored.password_hash)


def test_password_over_72_bytes_is_rejected_before_hashing() -> None:
    service = UserService(
        repository=InMemoryUserRepository(), hasher=BcryptPasswordHasher(rounds=4)
    )

    with pytest.raises(InvalidPasswordError, match="too long"):
        service.register("alice", "a" * 73)

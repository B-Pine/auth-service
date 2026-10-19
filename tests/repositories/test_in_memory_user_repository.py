import pytest

from auth.models import User
from auth.repositories.in_memory_user_repository import InMemoryUserRepository

ALICE = User(username="alice", password_hash="hash-a")


@pytest.fixture
def repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


def test_unknown_username_returns_none(repository: InMemoryUserRepository) -> None:
    assert repository.get("nobody") is None


def test_added_user_can_be_found(repository: InMemoryUserRepository) -> None:
    repository.add(ALICE)

    assert repository.get("alice") == ALICE


def test_each_repository_has_its_own_users() -> None:
    first = InMemoryUserRepository()
    second = InMemoryUserRepository()

    first.add(ALICE)

    assert second.get("alice") is None

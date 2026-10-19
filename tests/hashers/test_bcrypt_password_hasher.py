import pytest

from auth.hashers.bcrypt_password_hasher import BcryptPasswordHasher

PASSWORD = "correct-horse"


@pytest.fixture
def hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher(rounds=4)


def test_hash_does_not_contain_the_password(hasher: BcryptPasswordHasher) -> None:
    assert PASSWORD not in hasher.hash(PASSWORD)


def test_correct_password_verifies(hasher: BcryptPasswordHasher) -> None:
    password_hash = hasher.hash(PASSWORD)

    assert hasher.verify(PASSWORD, password_hash)


def test_wrong_password_does_not_verify(hasher: BcryptPasswordHasher) -> None:
    password_hash = hasher.hash(PASSWORD)

    assert not hasher.verify("wrong-password", password_hash)


def test_same_password_gets_a_different_hash_each_time(
    hasher: BcryptPasswordHasher,
) -> None:
    assert hasher.hash(PASSWORD) != hasher.hash(PASSWORD)


def test_hash_uses_the_configured_rounds() -> None:
    assert BcryptPasswordHasher(rounds=5).hash(PASSWORD).startswith("$2b$05$")


def test_default_rounds_are_12() -> None:
    assert BcryptPasswordHasher().hash(PASSWORD).startswith("$2b$12$")


@pytest.mark.parametrize(
    "bad_hash", ["", "not-a-hash", "$2b$04$tooshort", "é-not-ascii"]
)
def test_malformed_hash_does_not_verify(
    hasher: BcryptPasswordHasher, bad_hash: str
) -> None:
    assert not hasher.verify(PASSWORD, bad_hash)

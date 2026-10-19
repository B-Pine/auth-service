import pytest

from auth.exceptions import InvalidPasswordError
from auth.utils.validators import validate_password


@pytest.mark.parametrize(
    "password",
    [
        "a" * 72,  # 72 characters, 72 bytes
        "é" * 36,  # 36 characters, 72 bytes
    ],
)
def test_accepts_a_password_of_exactly_72_bytes(password: str) -> None:
    validate_password(password)


@pytest.mark.parametrize(
    "password",
    [
        "a" * 73,  # 73 characters, 73 bytes
        "é" * 37,  # only 37 characters, but 74 bytes
    ],
)
def test_rejects_a_password_longer_than_72_bytes(password: str) -> None:
    with pytest.raises(InvalidPasswordError, match="too long"):
        validate_password(password)

"""Validation rules shared across the authentication service."""

from auth.exceptions import InvalidPasswordError

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_BYTES = 72


def validate_password(password: str) -> None:
    """Check that a password meets the password policy.

    The policy requires at least ``MIN_PASSWORD_LENGTH`` characters and
    at most ``MAX_PASSWORD_BYTES`` bytes in UTF-8. The upper limit is
    bcrypt's: it only uses the first 72 bytes of a password.

    Args:
        password: The plain password to check.

    Raises:
        InvalidPasswordError: If the password is too short or too long.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise InvalidPasswordError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise InvalidPasswordError("Password is too long")

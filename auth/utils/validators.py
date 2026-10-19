"""Validation rules shared across the authentication service."""

from auth.exceptions import InvalidPasswordError

MIN_PASSWORD_LENGTH = 8


def validate_password(password: str) -> None:
    """Check that a password meets the password policy.

    The policy requires at least ``MIN_PASSWORD_LENGTH`` characters.

    Args:
        password: The plain password to check.

    Raises:
        InvalidPasswordError: If the password is too short.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise InvalidPasswordError(
            f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )

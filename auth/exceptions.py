"""Custom exceptions raised by the authentication service."""


class AuthError(Exception):
    """Base class for all authentication errors."""


class UserAlreadyExistsError(AuthError):
    """Raised when registering a username that is already taken.

    Attributes:
        username: The username that is already taken.
    """

    def __init__(self, username: str) -> None:
        """Initialize the error with the taken username.

        Args:
            username: The username that is already taken.
        """
        super().__init__(f"Username '{username}' is already taken")
        self.username = username

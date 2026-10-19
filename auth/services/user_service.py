"""User registration and login."""

from auth.exceptions import UserAlreadyExistsError, UserNotFoundError
from auth.hashers.password_hasher import PasswordHasher
from auth.models import User
from auth.repositories.user_repository import UserRepository
from auth.utils.validators import validate_password

MIN_PASSWORD_LENGTH = 8


class UserService:
    """Registers users and verifies their credentials."""

    def __init__(self, repository: UserRepository, hasher: PasswordHasher) -> None:
        """Create the service with the components it depends on.

        Args:
            repository: Where users are stored.
            hasher: How passwords are hashed and verified.
        """
        self._repository = repository
        self._hasher = hasher

    def register(self, username: str, password: str) -> User:
        """Register a new user.

        Args:
            username: The name the user will log in with.
            password: The user's chosen password.

        Returns:
            The registered user.

        Raises:
            InvalidPasswordError: If the password does not meet the policy.
            UserAlreadyExistsError: if the username is already taken.
        """
        validate_password(password)
        if self._repository.get(username) is not None:
            raise UserAlreadyExistsError(username)

        user = User(username=username, password_hash=self._hasher.hash(password))
        self._repository.add(user)
        return user

    def login(self, username: str, password: str) -> User:
        """Verify a user's credentials.

        Args:
            username: The username to log in with.
            password: The password to check.

        Returns:
            The user whose credentials were verified.

        Raises:
            UserNotFoundError: if no user has the username.
        """
        user = self._repository.get(username)
        if user is None:
            raise UserNotFoundError(username)
        raise NotImplementedError

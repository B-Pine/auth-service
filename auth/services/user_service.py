"""User registration and login."""

from auth.exceptions import UserAlreadyExistsError
from auth.hashers.password_hasher import PasswordHasher
from auth.models import User
from auth.repositories.user_repository import UserRepository


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
            UserAlreadyExistsError: if the username is already taken.
        """
        if self._repository.get(username) is not None:
            raise UserAlreadyExistsError(username)

        user = User(username=username, password_hash=self._hasher.hash(password))
        self._repository.add(user)
        return user

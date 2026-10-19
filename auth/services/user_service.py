"""User registration and login."""

import logging

from auth.exceptions import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from auth.hashers.password_hasher import PasswordHasher
from auth.models import User
from auth.repositories.user_repository import UserRepository
from auth.utils.validators import validate_password

MIN_PASSWORD_LENGTH = 8
logger = logging.getLogger(__name__)


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
        try:
            validate_password(password)
        except InvalidPasswordError:
            logger.warning(
                "registration rejected username=%s reason=weak_password", username
            )
            raise
        if self._repository.get(username) is not None:
            logger.warning(
                "registration rejected username=%s reason=username_taken", username
            )
            raise UserAlreadyExistsError(username)

        user = User(username=username, password_hash=self._hasher.hash(password))
        self._repository.add(user)
        logger.info("user registered username=%s", username)
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
            InvalidPasswordError: if the password is wrong.
        """
        user = self._repository.get(username)
        if user is None:
            logger.warning("login failed username=%s reason=unknown_user", username)
            raise UserNotFoundError(username)

        if not self._hasher.verify(password, user.password_hash):
            logger.warning("login failed username=%s reason=wrong_password", username)
            raise InvalidPasswordError("Incorrect password")
        logger.info("login succeeded username=%s", username)
        return user

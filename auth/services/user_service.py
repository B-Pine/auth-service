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

logger = logging.getLogger(__name__)


class UserService:
    """Registers users and verifies their credentials.

    The service holds the rules of registration and login. It depends
    only on the UserRepository and PasswordHasher interfaces, which are
    passed in when it is created, so storage and hashing can be replaced
    without changing it. Every registration and login attempt is logged;
    passwords and hashes never are.
    """

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
            UserAlreadyExistsError: If the username is already taken.
        """
        self._check_password_policy(username, password)
        self._check_username_available(username)
        user = User(username=username, password_hash=self._hasher.hash(password))
        self._repository.add(user)
        logger.info("user registered username=%s", username)
        return user

    def login(self, username: str, password: str) -> User:
        """Verify a user's credentials.

        The two failures raise different exceptions so that callers and
        logs can tell them apart. Anything shown to an end user should
        treat them the same, for example "Invalid username or password",
        so that it does not reveal which usernames exist.

        Args:
            username: The username to log in with.
            password: The password to check.

        Returns:
            The user whose credentials were verified.

        Raises:
            UserNotFoundError: If no user has the username.
            InvalidPasswordError: If the password is wrong.
        """
        user = self._find_user(username)
        self._check_password(user, password)
        logger.info("login succeeded username=%s", username)
        return user

    def _check_password_policy(self, username: str, password: str) -> None:
        """Reject a registration whose password does not meet the policy.

        Args:
            username: The username being registered, for the log.
            password: The chosen password.

        Raises:
            InvalidPasswordError: If the password does not meet the policy.
        """
        try:
            validate_password(password)
        except InvalidPasswordError:
            logger.warning(
                "registration rejected username=%s reason=weak_password", username
            )
            raise

    def _check_username_available(self, username: str) -> None:
        """Reject a registration whose username is already taken.

        Args:
            username: The username being registered.

        Raises:
            UserAlreadyExistsError: If the username is already taken.
        """
        if self._repository.get(username) is not None:
            logger.warning(
                "registration rejected username=%s reason=username_taken", username
            )
            raise UserAlreadyExistsError(username)

    def _find_user(self, username: str) -> User:
        """Find the user who is logging in.

        Args:
            username: The username to log in with.

        Returns:
            The user with that username.

        Raises:
            UserNotFoundError: If no user has the username.
        """
        user = self._repository.get(username)
        if user is None:
            logger.warning("login failed username=%s reason=unknown_user", username)
            raise UserNotFoundError(username)
        return user

    def _check_password(self, user: User, password: str) -> None:
        """Reject a login whose password does not match the stored hash.

        Args:
            user: The user who is logging in.
            password: The password to check.

        Raises:
            InvalidPasswordError: If the password is wrong.
        """
        if not self._hasher.verify(password, user.password_hash):
            logger.warning(
                "login failed username=%s reason=wrong_password", user.username
            )
            raise InvalidPasswordError("Incorrect password")

"""Abstract interface for user storage."""

from abc import ABC, abstractmethod

from auth.models import User


class UserRepository(ABC):
    """Stores users and finds them by username.

    The repository only stores and retrieves. Rules such as rejecting
    duplicate usernames belong to the service.
    """

    @abstractmethod
    def get(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to look up.

        Returns:
            The user, or None if no user has that username.
        """

    @abstractmethod
    def add(self, user: User) -> None:
        """Store a new user.

        Args:
            user: The user to store.
        """

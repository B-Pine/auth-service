"""User repository that keeps users in memory."""

from auth.models import User
from auth.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    """Keeps users in a dictionary for as long as the program runs.

    Useful for tests, demos, and as a reference implementation. Users
    are lost when the program ends; a database-backed repository would
    implement the same interface for permanent storage.
    """

    def get(self, username: str) -> User | None:
        """Find a user by username.

        Args:
            username: The username to look up.

        Returns:
            The user, or None if no user has that username.
        """
        raise NotImplementedError

    def add(self, user: User) -> None:
        """Store a new user.

        Args:
            user: The user to store.
        """
        raise NotImplementedError

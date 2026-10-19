"""Abstract interface for password hashing."""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Turns passwords into hashes and checks passwords against them."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Create a hash of a password.

        Args:
            password: The plain password.

        Returns:
            The hash to store instead of the password.
        """

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Check whether a password matches a stored hash.

        Args:
            password: The plain password to check.
            password_hash: A hash created earlier by ``hash``.

        Returns:
            True if the password matches the hash, otherwise False.
        """

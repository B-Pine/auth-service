"""Password hasher that uses bcrypt."""

import bcrypt

from auth.hashers.password_hasher import PasswordHasher

DEFAULT_ROUNDS = 12


class BcryptPasswordHasher(PasswordHasher):
    """Hashes passwords with bcrypt, a deliberately slow, salted algorithm.

    Each hash includes a random salt, so the same password produces a
    different hash every time. The cost grows with ``rounds``: each
    extra round doubles the work, making guessing attacks slower.
    """

    def __init__(self, rounds: int = DEFAULT_ROUNDS) -> None:
        """Create the hasher.

        Args:
            rounds: The bcrypt cost factor, from 4 to 31. The default of
                12 suits production; tests can use 4 to run fast.
        """
        self._rounds = rounds

    def hash(self, password: str) -> str:
        """Create a salted bcrypt hash of a password.

        Args:
            password: The plain password.

        Returns:
            The bcrypt hash, which includes its salt and cost factor.
        """
        salt = bcrypt.gensalt(rounds=self._rounds)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("ascii")

    def verify(self, password: str, password_hash: str) -> bool:
        """Check whether a password matches a bcrypt hash.

        Args:
            password: The plain password to check.
            password_hash: A hash created earlier by ``hash``.

        Returns:
            True if the password matches the hash, False if it does not,
            or if the stored hash is malformed: damaged hash must never
            let anyone in.
        """
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"), password_hash.encode("ascii")
            )
        except ValueError:
            return False

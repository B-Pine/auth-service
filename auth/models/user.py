"""User data model."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class User:
    """A registered user.

    Attributes:
        username: The name the user logs in with.
        password_hash: The hashed password. The plain password is never
            stored. It is left out of the text representation, so
            printing or logging a User does not reveal it.
    """

    username: str
    password_hash: str = field(repr=False)

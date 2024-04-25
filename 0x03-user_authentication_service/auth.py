#!/usr/bin/env python3
"""module for related-authentication routine
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes the input password using bcrypt.

        Args:
            password: A string representing the password to be hashed.

        Returns:
            bytes: A salted hash of the input password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user.

        Args:
            email: A string representing the user's email.
            password: A string representing the user's password.

        Returns:
            User: A User object representing the registered user.

        Raises:
            ValueError: If a user already exists with the passed email.
        """
        # Check if user already exists
        if self._db.find_user_by_email(email):
            raise ValueError(f"User {email} already exists")

        # Hash the password
        hashed_password = self._hash_password(password)

        # Create a new User object
        user = User(email, hashed_password)

        # Save the user to the database
        self._db.add_user(user)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email: A string representing the user's email.
            password: A string representing the user's password.

        Returns:
            bool: True if the login credentials are valid, False otherwise.
        """
        user = self._db.find_user_by_email(email)
        if user:
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        return False

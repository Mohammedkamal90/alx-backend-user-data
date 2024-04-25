#!/usr/bin/env python3
"""module related authentication routines
"""
import bcrypt
from db import DB
from user import User
from auth import _hash_password

def _hash_password(password: str) -> bytes:
    """
    Hashes a password string using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a salted hash of the input password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

# Example usage
if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))

class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        # Check if user with email already exists
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists")

        # Hash the password
        hashed_password = _hash_password(password)

        # Save the user to the database
        user = self._db.add_user(email, hashed_password)

        return user

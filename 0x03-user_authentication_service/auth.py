#!/usr/bin/env python3
"""module for related-authentication routine
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hashes password string using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the input password.
    """
    # Generate a salted hash of the input password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

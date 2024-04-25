#!/usr/bin/env python3
"""module related authentication routines
"""
import bcrypt

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

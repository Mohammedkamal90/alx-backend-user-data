#!/usr/bin/env python3
"""
authentication module
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """Class to manage Basic Authentication."""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header: The Authorization header.

        Returns:
            The Base64 part of the Authorization header if present, otherwise None.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 encoded string.

        Args:
            base64_authorization_header: The Base64 encoded string.

        Returns:
            The decoded string if successfully decoded, otherwise None.
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials from the decoded Base64 string.

        Args:
            decoded_base64_authorization_header: The decoded Base64 string.

        Returns:
            A tuple containing the user email and password if successfully extracted, otherwise (None, None).
        """
        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Get the User instance based on email and password.

        Args:
            user_email: The user's email.
            user_pwd: The user's password.

        Returns:
            The User instance if found and password matches, otherwise None.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        users = User.search({"email": user_email})
        if not users:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user based on Basic Authentication.

        Args:
            request: The Flask request object.

        Returns:
            The current User instance if authenticated, otherwise None.
        """
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_auth = self.extract_base64_authorization_header(authorization_header)
        if base64_auth is None:
            return None
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None
        return self.user_object_from_credentials(user_email, user_pwd)

#!/usr/bin/env python3
"""Authentication module for API"""

import re
import base64
from .auth import Auth
from models.user import User
import binascii
from typing import Tuple, Optional, TypeVar


class BasicAuth(Auth):
    """authentication class"""
    
    @staticmethod
    def extract_base64_authorization_header(authorization_header: str) -> Optional[str]:
        """extract a Base64 part of a Authorization header for a Basic Authentication."""
        match = re.match(r'Basic\s+(.+)', authorization_header.strip())
        return match.group(1) if match else None

    @staticmethod
    def decode_base64_authorization_header(base64_authorization_header: str) -> Optional[str]:
        """decode base64-encoded authorization header"""
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    @staticmethod
    def extract_user_credentials(decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """extract user credential from base64-decoded authorization header"""
        match = re.match(r'(?P<user>[^:]+):(?P<password>.+)', decoded_base64_authorization_header.strip())
        return match.group('user', 'password') if match else (None, None)

    @staticmethod
    def user_object_from_credentials(user_email: str, user_pwd: str) -> Optional[User]:
        """retrieve user based on user's authentication credential"""
        users = User.search({'email': user_email})
        if users and users[0].is_valid_password(user_pwd):
            return users[0]
        return None

    def current_user(self, request=None) -> Optional[User]:
        """retrieve user from request"""
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)

#!/usr/bin/env python3
"""authentication module for API"""

import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Class for managing API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given path.

        Args:
            path: path to check for authentication requirement.
            excluded_paths: List of paths that are excluded from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Gets authorization header field from the request.

        Args:
            request: Flask request object.

        Returns:
            str: Value of authorization header, or None if not present.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets current user from the request.

        Args:
            request: flask request object.

        Returns:
            TypeVar('User'): current user, or None if not available.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Gets value of the cookie named SESSION_NAME.

        Args:
            request: Flask request object.

        Returns:
            str: value of session cookie, or None if not found.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)

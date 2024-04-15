#!/usr/bin/env python3
"""
authentication module
"""
from typing import List, TypeVar
from flask import request, abort
from models.user import User


class Auth:
    """Class manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if path requires authentication

        Args:
            path: path to check
            excluded_paths: list of paths that are exempt from authentication.

        Returns:
            True if authentication is required, False otherwise
        """
        if path is None or not excluded_paths:
            return True
        for excluded_path in excluded_paths:
            if path == excluded_path or (excluded_path.endswith("*") and path.startswith(excluded_path[:-1])):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieve Authorization header from the request

        Args:
            request: Flask request object

        Returns:
             value of the Authorization header if present, otherwise None
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            current user if authenticated, otherwise None.
        """
        return None

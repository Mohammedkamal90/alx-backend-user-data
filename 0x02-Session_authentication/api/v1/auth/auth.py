#!/usr/bin/env python3
"""
module for Authentication
"""
from flask import request
import os

class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require authentication"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        
        if path[-1] != '/':
            path += '/'

        for ep in excluded_paths:
            if ep.endswith('*') and path.startswith(ep[:-1]):
                return False
            elif path == ep:
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """Get Authorization header from the request"""
        if request is None or 'Authorization' not in request.headers:
            return None
        
        return request.headers['Authorization']

    def session_cookie(self, request=None) -> str:
        """Get value of session cookie from request"""
        if request is None:
            return None
        
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)

#!/usr/bin/env python3
"""
module Session Authentication
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session Authentication"""

    def __init__(self):
        """Constructor"""
        super().__init__()

    def current_user(self, request=None):
        """Return current user based on session cookie"""
        if request is None:
            return None

        # Get session cookie value
        session_cookie_value = self.session_cookie(request)

        # If session cookie is None, return None
        if session_cookie_value is None:
            return None

        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        user = User.get(user_id)

        return user

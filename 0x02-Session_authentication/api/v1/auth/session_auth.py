#!/usr/bin/env python3
"""
module Session Authentication
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth

class SessionAuth(Auth):
    """
    SessionAuth class
    """

    def __init__(self):
        """
        Initialize SessionAuth instance
        """
        super().__init__()

    def current_user(self, request=None):
        """
        Return the User instance based on the cookie value
        """
        if request is None:
            return None

        session_id = self.session_cookie(request)

        if session_id is None:
            return None

        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return None

        user = User.get(user_id)

        return user

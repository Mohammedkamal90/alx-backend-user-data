#!/usr/bin/env python3
"""Module for SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database"""

    def create_session(self, user_id=None):
        """Create a session and store in the database"""
        session_id = super().create_session(user_id)
        if session_id:
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieve user id for session from the database"""
        if session_id is None:
            return None

        user_session = UserSession.search({'session_id': session_id})
        if user_session:
            user_session = user_session[0]
            if self.session_duration <= 0:
                return user_session.user_id

            created_at = user_session.created_at
            if created_at is None:
                return None

            expiration_time = created_at + timedelta(seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None

            return user_session.user_id
        return None

    def destroy_session(self, request=None):
        """Destroy a session from the database"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id:
            sessions = UserSession.search({'session_id': session_id})
            if sessions:
                for session in sessions:
                    session.delete()
                return True
        return False

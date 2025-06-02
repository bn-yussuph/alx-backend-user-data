#!/usr/bin/env python3
""" Module Session_auth for user authentication
"""
from typing import TypeVar, Tuple
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Extends BasicAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id:
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return session ID based on user ID
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """ Return a user_id
        """
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        return User.get(session_user_id)

    def destroy_session(self, request=None):
        """Delete the user session /logout"""

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True

#!/usr/bin/env python3
"""" Auth module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> str:
    """ Return a salted hash of the password
    """
    bytes = password.encode()
    salt = bcrypt.gensalt()

    hpw = bcrypt.hashpw(bytes, salt)

    return hpw


def _generate_uuid() -> str:
    """ Generate a uuid code
    Args: None
    Returns: a uuid code as a string
    """
    code = uuid.uuid4()
    return str(code)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Rregister a user and return same
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hspw = _hash_password(password)
            new_user = self._db.add_user(email, hspw)
            return new_user
        else:
            raise ValueError(f'User {email} already exists.')

    def valid_login(self, email: str, password: str) -> bool:
        """ Check for valid credentials
        Args: email amd password
        Return: bool
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        encoded_password = password.encode()

        if bcrypt.checkpw(encoded_password, user_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """ Find a user and create a seesion for him
        Args: email
        Return: session Id or None
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        ses_id = _generate_uuid()

        self._db.update_user(user.id, session_id=ses_id)

        return ses_id

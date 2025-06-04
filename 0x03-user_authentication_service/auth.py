#!/usr/bin/env python3
"""" Auth module
"""
import bcrypt
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

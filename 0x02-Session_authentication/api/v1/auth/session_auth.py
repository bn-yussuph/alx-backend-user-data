#!/usr/bin/env python3
""" Module Session_auth for user authentication
"""
from typing import TypeVar, Tuple
from base64 import b64decode, decode
from api.v1.auth.auth import Auth
from models.user import User
import base64


class SessionAuth(Auth):
    """ Extends BasicAuth class
    """


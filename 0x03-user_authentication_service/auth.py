#!/usr/bin/env python3
"""" Auth module
"""
import bcrypt


def _hash_password(password: str) -> str:
    """ Return a salted hash of the password
    """
    bytes = password.encode()
    salt = bcrypt.gensalt()

    hpw = bcrypt.hashpw(bytes, salt)

    return hpw

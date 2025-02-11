import hashlib
import os
import secrets
from typing import Tuple

from pydantic import SecretStr


def hash_password(password: SecretStr | str) -> Tuple[bytes, bytes]:
    # Generate a random salt
    salt = os.urandom(16)
    # Hash the password with the salt
    hashed_password: bytes = hashlib.pbkdf2_hmac(
        "sha256",  # Hashing algorithm
        password.get_secret_value().encode("UTF-8")
        if isinstance(password, SecretStr)
        else password.encode("UTF-8"),
        salt,
        100000,  # Number of iterations
    )

    return salt, hashed_password


def verify_password(
    stored_password: bytes, stored_salt: bytes, given_password: str
) -> bool:
    """
    Verify stored password against stored salt.

    :param stored_password: stored password.
    :param stored_salt: stored salt.
    :param given_password: password.
    :return: True if stored password matches stored salt.

    """
    give_password = hashlib.pbkdf2_hmac(
        "sha256",
        iterations=100000,
        password=given_password.encode("utf-8"),
        salt=stored_salt,
    )
    return secrets.compare_digest(give_password, stored_password)

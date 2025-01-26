import hashlib
import os
import secrets


def hash_password(password):
    # Generate a random salt
    salt = os.urandom(16)

    # Hash the password with the salt
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',  # Hashing algorithm
        password.encode('utf-8'),  # Convert password to bytes
        salt,  # Salt
        100000  # Number of iterations
    )

    return salt, hashed_password


def verify_password(stored_password: bytes, stored_salt: str, given_password: str) -> bool:
    give_password = hashlib.pbkdf2_hmac(password=given_password.encode('utf-8'), salt=stored_salt)
    return secrets.compare_digest(give_password, stored_password)

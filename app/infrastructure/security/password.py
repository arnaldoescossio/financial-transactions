import bcrypt

from app.core.config.env_config import settings

# bcrypt has a hard limit of 72 bytes per password
_PASSWORD_MAX_BYTES = 72


def hash_password(plain: str) -> str:
    """
    Hash a password using bcrypt.

    Note: bcrypt has a 72-byte limit. Passwords longer than this are truncated.
    This is safe because we also validate password length in schemas.
    """
    # Truncate to 72 bytes if necessary (bcrypt requirement)
    truncated = plain.encode("utf-8")[:_PASSWORD_MAX_BYTES]
    bcrypt_rounds = getattr(settings, "bcrypt_rounds", 12)
    salt = bcrypt.gensalt(rounds=bcrypt_rounds)
    hashed = bcrypt.hashpw(truncated, salt)
    return hashed.decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a plain password against a bcrypt hash.

    Note: Apply the same 72-byte truncation as hash_password for consistency.
    """
    # Truncate to 72 bytes if necessary (must match hashing logic)
    truncated = plain.encode("utf-8")[:_PASSWORD_MAX_BYTES]
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(truncated, hashed_bytes)

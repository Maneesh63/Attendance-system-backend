
import hashlib
import os
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def hash_password(password: str, salt: str = None) -> str:
    """Hashes a password using SHA-256 with a salt."""
    if salt is None:
        salt = os.urandom(16).hex()  # Generate a random 16-byte salt

    hash_obj = hashlib.sha256((salt + password).encode())
    hashed_password = hash_obj.hexdigest()
    return f"{salt}${hashed_password}"  # Store salt and hash together


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verifies a password against a stored hash (salt$hash format)."""
    salt, correct_hash = stored_hash.split("$")
    return hash_password(plain_password, salt) == stored_hash

def date_and_time():
    now = datetime.now()
    now_utc = datetime.now(timezone.utc)
    now_ist = now_utc.astimezone(ZoneInfo("Asia/Kolkata"))
    return {
        "now": now,
        "now_utc": now_utc,
        "now_ist": now_ist,
    }
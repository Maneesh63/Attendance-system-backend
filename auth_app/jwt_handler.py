import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
import json
from zoneinfo import ZoneInfo
import uuid

ALGORITHM = "HS256"


def generate_jwt(user):
    now = datetime.now(timezone.utc)
    payload = {
        "jti": str(uuid.uuid4()),
        "user_id": str(user.user_id),
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=5)).timestamp()),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token, user.user_id, user.email


def decode_jwt(token):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

import jwt

from django.conf import settings

from datetime import datetime, timezone, timedelta
import logging

logger = logging.getLogger(__name__)

def generate_token(payload: dict, expires_in: timedelta) -> str:
    payload.update({"exp": datetime.now(tz=timezone.utc) + expires_in})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def validate_token(jwt_token: str) -> dict:
    try:
        return jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError as e:
        return {"message": "Token expired"}

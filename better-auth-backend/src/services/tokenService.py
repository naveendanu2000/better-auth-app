import jwt
from datetime import timedelta, datetime, timezone
import os

ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET = os.getenv("JWT_SECRET")


def create_access_token(id: int, expires_delta: timedelta | None):
    to_encode = {"id": id}.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(payload=to_encode, key=JWT_SECRET, algorithm=ALGORITHM)

import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import timedelta, datetime, timezone
import os
from fastapi import HTTPException, status, Cookie

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


def verify_access_token(token: str = Cookie()) -> dict:

    try:
        payload = jwt.decode(token, key=JWT_SECRET, algorithms=ALGORITHM)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    return payload

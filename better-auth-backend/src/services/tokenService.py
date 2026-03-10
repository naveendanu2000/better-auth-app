import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import timedelta, datetime, timezone
import os
from fastapi import HTTPException, status, Cookie
from src.schemas.tokenDTO import tokenPayloadData


ALGORITHM = os.getenv("ALGORITHM")
JWT_SECRET = os.getenv("JWT_SECRET")


def create_access_token(id: int, expires_delta: timedelta | None):
    to_encode = {"id": id}.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": int(expire.timestamp())})

    if JWT_SECRET:
        return jwt.encode(payload=to_encode, key=JWT_SECRET, algorithm=ALGORITHM)
    else:
        raise HTTPException(status_code=500, detail="Internal server error")


def verify_access_token(access_token: str = Cookie()) -> tokenPayloadData:

    try:
        if JWT_SECRET:
            payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=ALGORITHM)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Expired"
        )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    return tokenPayloadData(**payload)

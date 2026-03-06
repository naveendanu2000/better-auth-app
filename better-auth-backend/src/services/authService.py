import asyncpg
from src.schemas.authDTO import signupPayload, signinPayload, signupResponseDTO
from src.services.password_service import verifyPassword
from fastapi.exceptions import HTTPException
from asyncpg.exceptions import UniqueViolationError


async def loginUser(
    conn: asyncpg.Connection, payload: signinPayload
) -> signupResponseDTO | None:

    result = await conn.fetchrow(
        "SELECT id, username, email, password FROM public.users where username=$1",
        payload.username,
    )

    # print(result)

    if not result:
        verifyPassword(payload.password, None)
        raise HTTPException(status_code=401, detail="username or password incorrect")

    if verifyPassword(payload.password, result["password"]):
        return signupResponseDTO(**dict(result))
    else:
        raise HTTPException(status_code=401, detail="username or password incorrect")


async def createUser(
    conn: asyncpg.Connection, payload: signupPayload
) -> signupResponseDTO | None:
    try:
        result = await conn.fetchrow(
            "INSERT INTO public.users(username, email, password) VALUES ($1, $2, $3) RETURNING id,username,email",
            payload.username,
            payload.email,
            payload.password,
        )
    except UniqueViolationError:
        raise HTTPException(status_code=409, detail="User already exists!")

    if result:
        return signupResponseDTO(**dict(result))

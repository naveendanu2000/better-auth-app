import asyncpg
from src.schemas.authDTO import (
    signupPayload,
    signinPayload,
    signupResponseDTO,
    googleUserRegisterPayload,
)
from src.services.password_service import verifyPassword
from fastapi.exceptions import HTTPException
from asyncpg.exceptions import UniqueViolationError, NoDataFoundError
from fastapi import status


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
        user_result = await conn.fetchrow(
            "INSERT INTO public.users(username, email, password) VALUES ($1, $2, $3) RETURNING id,username,email",
            payload.username,
            payload.email,
            payload.password,
        )
        if user_result:
            await conn.fetchrow(
                "INSERT INTO public.user_ids(user_id, provider, password)	VALUES ($1, 'local', $2)",
                user_result.id,
                payload.password,
            )

    except UniqueViolationError:
        raise HTTPException(status_code=409, detail="User already exists!")

    if user_result:
        return signupResponseDTO(**dict(user_result))


async def googleUserRegister(
    conn: asyncpg.Connection, payload: googleUserRegisterPayload
):

    result = await conn.fetchrow(
        "select id from public.users where email=$1", payload.email
    )

    if not result:
        result = await conn.fetchrow(
            "INSERT INTO public.users(username, email) values($1, $2) RETURNING id",
            payload.username,
            payload.email,
        )

    if result:
        result_dict = dict(result)
        # print(result_dict)
        row = await conn.fetchrow(
            "INSERT INTO public.user_ids(user_id, provider_user_id, provider) values($1, $2, 'Google') RETURNING user_id",
            result_dict["id"],
            str(object=payload.provider_user_id),
        )

        if row:
            return int(row["user_id"])


async def getUserById(conn: asyncpg.Connection, userid: int) -> dict | None:
    try:
        result = await conn.fetchrow(
            "SELECT id, username, email, created_at from public.users where id = $1",
            userid,
        )

    except NoDataFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT, detail="No data found"
        )

    if result:
        return dict(result)
    return None

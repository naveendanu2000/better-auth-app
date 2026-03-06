import asyncpg
from src.schemas.SignupSchema import signupPayload


async def createUser(conn: asyncpg.Connection, payload: signupPayload):
    try:
        result = await conn.fetchrow(
            "INSERT INTO public.users(username, email, password) VALUES ($1, $2, $3) RETURNING id,username,email",
            payload.username,
            payload.email,
            payload.password,
        )
        print(result)
        if result:
            return dict(result)
    except Exception as e:
        print(f"Unable to save the data! {e}")
        raise e

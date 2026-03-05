import asyncpg
from src.schemas.SignupSchema import signupPayload


async def createUser(conn: asyncpg.Connection, payload: signupPayload):
    result = conn.execute("INSERT INTO ")

from fastapi import APIRouter, Request
from schemas.SignupSchema import signupPayload
from src.services.password_service import hashPassword
from src.services.authService import createUser

router = APIRouter()


@router.post("/auth/login")
async def login():
    return


@router.post("/auth/signup")
async def signup(payload: signupPayload, request: Request):
    hashed_password = hashPassword(payload.password)
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        try:
            payload.password = hashed_password
            user = await createUser(
                conn=conn,
                payload=payload
            )
        except Exception as e:
            print(f"Unable to create User!{e}")

    return user

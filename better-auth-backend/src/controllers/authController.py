from fastapi import APIRouter, Request
from src.schemas.SignupSchema import signupPayload
from src.schemas.signupResponseDTO import signupResponseDTO
from src.services.password_service import hashPassword
from src.services.authService import createUser

router = APIRouter()


@router.post("/api/auth/login")
async def login():
    return


@router.post("/api/auth/signup", response_model=signupResponseDTO)
async def signup(payload: signupPayload, request: Request):
    hashed_password = hashPassword(payload.password)
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        try:
            payload.password = hashed_password
            user = await createUser(conn=conn, payload=payload)
            if user:
                return user
        except Exception as e:
            print(f"Unable to create User!{e}")
            raise e

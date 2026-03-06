from fastapi import APIRouter, Request
from src.schemas.authDTO import signupResponseDTO, signupPayload, signinPayload
from src.services.password_service import hashPassword
from src.services.authService import createUser, loginUser
from src.services.tokenService import create_access_token
from fastapi.responses import JSONResponse
from src.responses.global_response_wrapper import success_response, cookieSchema

router = APIRouter()


@router.post("/api/auth/login")
async def login(payload: signinPayload, request: Request):
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        user = await loginUser(conn=conn, payload=payload)
        if user:
            jwt_token = create_access_token(id=user.id, expires_delta=None)

        if jwt_token:
            return success_response(
                data=None,
                message="Login successfull",
                cookie=cookieSchema(key="access_token", value=jwt_token),
            )


@router.post("/api/auth/signup", response_model=signupResponseDTO)
async def signup(payload: signupPayload, request: Request):
    hashed_password = hashPassword(payload.password)
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        payload.password = hashed_password
        user = await createUser(conn=conn, payload=payload)
        return user

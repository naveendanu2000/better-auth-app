from fastapi import APIRouter, Request, Depends, HTTPException
from src.schemas.authDTO import (
    signupResponseDTO,
    signupPayload,
    signinPayload,
    googleUserRegisterPayload,
)
from src.services.password_service import hashPassword
from src.services.authService import (
    createUser,
    loginUser,
    googleUserRegister,
    getUserById,
)
from src.services.tokenService import create_access_token, verify_access_token
from src.responses.global_response_wrapper import success_response, cookieSchema
from authlib_config import oauth
from datetime import timedelta
from src.schemas.tokenDTO import tokenPayloadData

router = APIRouter(prefix="/api/auth")


@router.post("/login")
async def login(payload: signinPayload, request: Request):
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        user = await loginUser(conn=conn, payload=payload)
        print(user)
        if user:
            jwt_token = create_access_token(id=user.id, expires_delta=None)
            print("\nthis is the jwt token" + jwt_token)
            if jwt_token:
                return success_response(
                    data=None,
                    message="Login successfull",
                    cookie=cookieSchema(key="access_token", value=jwt_token),
                )


@router.get("/login/google")
async def login_google(request: Request):

    redirect_uri = request.url_for(
        "login_google_callback"
    )  # login_google_callback is the name of the function for the call_back URI

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/login/google/callback")
async def login_google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]
    print(user_info)

    jwt_token = create_access_token(user_info["email"], timedelta(minutes=15))

    pool = request.app.state.pool

    async with pool.acquire() as conn:
        await googleUserRegister(
            conn=conn,
            payload=googleUserRegisterPayload(
                username=user_info["name"],
                email=user_info["email"],
                provider_user_id=user_info["sub"],
            ),
        )

    return success_response(
        data={"email": user_info["email"], "name": user_info["name"]},
        message="Login Successful",
        cookie=cookieSchema(key="access_token", value=jwt_token),
    )


@router.post("/signup", response_model=signupResponseDTO)
async def signup(payload: signupPayload, request: Request):
    hashed_password = hashPassword(payload.password)
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        payload.password = hashed_password
        user = await createUser(conn=conn, payload=payload)
        return success_response(
            data=user.model_dump() if user else None,
            message="Signup successful",
            cookie=None,
        )


@router.get("/current/user")
async def getCurrentUser(
    request: Request, user: tokenPayloadData = Depends(verify_access_token)
):
    pool = request.app.state.pool

    async with pool.acquire() as conn:
        userData = await getUserById(conn=conn, userid=user.id)
        return success_response(
            data=userData,
            message="User details fetched successfully",
            cookie=None,
        )

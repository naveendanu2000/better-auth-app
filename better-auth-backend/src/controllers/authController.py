from fastapi import APIRouter, Request, Response, Depends
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
import threading
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/api/auth")


def printDone():
    print("Done")


@router.post("/login")
async def login(payload: signinPayload, request: Request):
    pool = request.app.state.pool
    t = threading.Timer(1, printDone)
    t.start()
    t.join()

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
async def login_google_callback(request: Request, response: Response):
    token = await oauth.google.authorize_access_token(request)

    user_info = token["userinfo"]
    print(user_info)

    pool = request.app.state.pool

    async with pool.acquire() as conn:
        user_id: int | None = await googleUserRegister(
            conn=conn,
            payload=googleUserRegisterPayload(
                username=user_info["name"],
                email=user_info["email"],
                provider_user_id=user_info["sub"],
            ),
        )

    if user_id:
        jwt_token = create_access_token(user_id, timedelta(minutes=15))

    response = RedirectResponse(url="http://localhost:5173/user", status_code=302)

    if jwt_token:
        response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            secure=False,
            samesite="lax",
            path="/",
            domain="localhost",
        )
    else:
        return {
            "success": False,
            "data": None,
            "message": "Unable to login internale server error",
        }

    return response


@router.post("/signup", response_model=signupResponseDTO)
async def signup(payload: signupPayload, request: Request):
    hashed_password = hashPassword(payload.password)
    pool = request.app.state.pool

    t = threading.Timer(1, printDone)
    t.start()
    t.join()

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

    t = threading.Timer(1, printDone)
    t.start()
    t.join()

    async with pool.acquire() as conn:
        userData = await getUserById(conn=conn, userid=user.id)
        return success_response(
            data=userData,
            message="User details fetched successfully",
            cookie=None,
        )


@router.get("/logout")
def logout(response: Response, user: tokenPayloadData = Depends(verify_access_token)):
    t = threading.Timer(1, printDone)
    t.start()
    t.join()
    if user:

        response = success_response(
            data=None, message="User logged out successfully", cookie=None
        )
        response.delete_cookie(key="access_token", path="/")
        return response

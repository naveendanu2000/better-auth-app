from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException
from fastapi import Request
from pydantic import BaseModel


class cookieSchema(BaseModel):
    key: str
    value: str


def success_response(data: dict | None, message: str, cookie: cookieSchema | None):
    response = JSONResponse(content={"sucesss": True, "data": data, "message": message})

    if cookie:
        response.set_cookie(
            key=cookie.key,
            value=cookie.value,
            httponly=True,
            secure=False,
            samesite="lax",
        )

    return response


async def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, HTTPException):
        response = await http_exception_handler(request=request, exc=exc)

        return JSONResponse(
            status_code=response.status_code,
            content={"success": False, "message": exc.detail, "data": None},
        )

    return JSONResponse(status_code=500, content={"message": "Internal server error!"})

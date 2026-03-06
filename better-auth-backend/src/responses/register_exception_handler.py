from fastapi import FastAPI, HTTPException, exceptions
from src.responses.global_response_wrapper import global_exception_handler


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, global_exception_handler)
    app.add_exception_handler(
        exceptions.RequestValidationError, global_exception_handler
    )

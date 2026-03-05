from pydantic import BaseModel


class signupPayload(BaseModel):
    username: str
    email: str
    password: str

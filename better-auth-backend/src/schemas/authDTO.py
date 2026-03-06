from pydantic import BaseModel


class signupPayload(BaseModel):
    username: str
    email: str
    password: str


class signupResponseDTO(BaseModel):
    id: int
    username: str
    email: str


class signinPayload(BaseModel):
    username: str
    password: str

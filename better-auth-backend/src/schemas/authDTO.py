from pydantic import BaseModel, Field, EmailStr


class signupPayload(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    email: EmailStr
    password: str = Field(min_length=5, max_length=16)


class signupResponseDTO(BaseModel):
    id: int
    username: str
    email: str


class signinPayload(BaseModel):
    username: str = Field(min_length=3, max_length=16)
    password: str = Field(min_length=5, max_length=16)


class googleUserRegisterPayload(BaseModel):
    username: str
    email: EmailStr
    provider_user_id: int

from pydantic import BaseModel


class signupResponseDTO(BaseModel):
    id: int
    username: str
    email: str

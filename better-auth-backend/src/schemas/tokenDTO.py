from pydantic import BaseModel


class tokenPayloadData(BaseModel):
    id: int
    exp: int

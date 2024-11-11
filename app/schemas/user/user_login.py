from pydantic import BaseModel


class LoginSubmit(BaseModel):
    message: str
    id: int

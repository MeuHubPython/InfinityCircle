from pydantic import BaseModel


class LoginSubmit(BaseModel):
    message: str
    email: str

from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    email: str
    password: str
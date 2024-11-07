from pydantic import BaseModel, EmailStr
from fastapi import Form


class CreateUser(BaseModel):
    name: str = Form()
    email: EmailStr = Form()
    password: str = Form()

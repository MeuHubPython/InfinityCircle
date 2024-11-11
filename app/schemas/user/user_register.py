from pydantic import BaseModel, EmailStr
from fastapi import Form


class CreateUser(BaseModel):
    profile_image: bytes | None = None
    image_format: str | None = None
    name: str = Form()
    email: EmailStr = Form()
    password: str = Form()

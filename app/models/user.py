from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    age: int | None = None
    description: str | None = None
    email: str = Field(unique=True)
    password: bytes
    profile_image: bytes | None = None
    image_format: str | None = None
    image_encoded: str | None = None
    created_at: str = datetime.now().strftime("%D %H:%M")

from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    image_encoded: str | None = None
    name: str
    age: int | None = None
    description: str | None = None
    email: str = Field(unique=True)
    password: bytes
    created_at: str = datetime.now().strftime("%D %H:%M")

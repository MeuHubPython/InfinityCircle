from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    email: str = Field(unique=True)
    password: bytes
    profile_image: bytes | None = None
    image_format: str | None = None

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    image_encoded: str | None = None
    color: str = Field(unique=True)
    name: str
    age: int | None = None
    description: str | None = None
    email: str = Field(unique=True)
    password: bytes
    created_at: str = datetime.now().strftime("%D %H:%M")

    posts: list["Post"] = Relationship(back_populates="user", cascade_delete=True)  # type: ignore
    comments: list["Comment"] = Relationship(back_populates="user")  # type: ignore
    flows: list["Flow"] = Relationship(back_populates="user", cascade_delete=True)  # type: ignore
    mentions: list["Mention"] = Relationship(back_populates="user")  # type: ignore

    flows_count: int = 0
    posts_count: int = 0
    comments_count: int = 0

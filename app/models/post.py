from sqlmodel import SQLModel, Field, Relationship
from models.user import User
from datetime import datetime


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    body: str
    created_at: str = datetime.now().strftime("%D %H:%M")

    user: User = Relationship(back_populates="posts")
    comments: list["Comment"] = Relationship(back_populates="post", cascade_delete=True)  # type: ignore
    flows: list["Flow"] = Relationship(back_populates="post")  # type: ignore

    comments_count: int = 0
    flows_count: int = 0

from sqlmodel import SQLModel, Field, Relationship
from models.user import User
from models.post import Post
from typing import Optional


class Mention(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int | None = Field(foreign_key="post.id", default=None)
    comment_id: int | None = Field(foreign_key="comment.id", default=None)

    user: User = Relationship(back_populates="mentions")
    post: Optional[Post] = Relationship(back_populates="mentions")
    comment: Optional["Comment"] = Relationship(back_populates="mentions")  # type: ignore

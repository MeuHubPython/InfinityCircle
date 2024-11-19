from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class Flow(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int | None = Field(foreign_key="post.id", default=None)
    comment_id: int | None = Field(
        foreign_key="comment.id", default=None, nullable=True
    )
    created_at: str = datetime.now().strftime("%D %H:%M")

    user: Optional["User"] = Relationship(back_populates="flows")  # type: ignore
    post: Optional["Post"] = Relationship(back_populates="flows")  # type: ignore
    comment: Optional["Comment"] = Relationship(back_populates="flows")  # type: ignore

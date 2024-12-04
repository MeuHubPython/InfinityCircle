from sqlmodel import SQLModel, Field, Relationship
from models.post import Post
from models.user import User
from typing import Optional
from datetime import datetime


class Comment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    body: str
    created_at: str = datetime.now().strftime("%D %H:%M")

    user: User = Relationship(back_populates="comments")  # type: ignore
    post: Optional[Post] = Relationship(back_populates="comments")
    flows: list["Flow"] = Relationship(back_populates="comment")  # type: ignore
    mentions: list["Mention"] = Relationship(back_populates="comment")  # type: ignore

    flows_counts: int = 0
    comments_counts: int = 0


# Usar Relationships e Cascade delete em comentarios, posts, users, pensar nisso amanhã!!!

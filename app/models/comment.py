from sqlmodel import SQLModel, Field


class Comment(SQLModel):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    post_id: int = Field(foreign_key="post.id")
    comment: str
    flows: int = 0


# Usar Relationships e Cascade delete em comentarios, posts, users, pensar nisso amanhã!!!

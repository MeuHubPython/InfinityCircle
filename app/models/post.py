from sqlmodel import SQLModel, Field, select
from models.user import User
from datetime import datetime


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user_name: str
    title: str
    body: str
    created_at: str = datetime.now().strftime("%D %H:%M")
    profile_image: str | None = None
    flows: int = 0
    comments: int = 0

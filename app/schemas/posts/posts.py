from pydantic import BaseModel
from datetime import datetime


class CreatedPost(BaseModel):
    mentions: str | None
    title: str
    body: str

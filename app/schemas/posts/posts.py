from pydantic import BaseModel
from datetime import datetime


class CreatedPost(BaseModel):
    title: str
    body: str

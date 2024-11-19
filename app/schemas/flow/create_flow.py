from pydantic import BaseModel
from datetime import datetime


class CreateFlow(BaseModel):
    user_id: int
    post_id: int | None
    comment_id: int | None
    created_at: str = datetime.now().strftime("%D %H:%M")

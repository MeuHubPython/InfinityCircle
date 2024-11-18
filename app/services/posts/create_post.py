from fastapi import Request
from fastapi.responses import RedirectResponse
from schemas.posts.posts import CreatedPost
from sqlmodel import Session, select
from models.post import Post
from models.user import User
import jwt, os
from datetime import datetime


async def create_post(request: Request, new_post: CreatedPost, session: Session):
    payload = jwt.decode(
        request.session["Authorization"],
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")],
    )

    post = Post(
        title=new_post.title,
        body=new_post.body,
        user_id=payload["id"],
        user_name=session.exec(select(User).where(User.id == payload["id"])).one().name,
        created_at=datetime.now().strftime("%D %H:%M"),
        profile_image=session.exec(select(User).where(User.id == payload["id"]))
        .one()
        .image_encoded,
    )
    session.add(post)
    session.commit()
    return RedirectResponse("/connections/", status_code=302)

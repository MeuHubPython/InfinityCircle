from fastapi import Request, Depends
from sqlmodel import Session, select
from database.init_db import get_session
from models.post import Post
from models.user import User
from fastapi.templating import Jinja2Templates
import jwt, os, asyncio


async def all_posts(request: Request, session: Session):
    post_db = session.exec(select(Post)).all()
    posts = []

    for post in post_db:
        posts.append(post)

    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )
    user = session.exec(select(User).where(User.id == payload["id"])).one()

    return Jinja2Templates(directory="templates").TemplateResponse(
        request,
        "connections.html",
        context={
            "posts": posts,
            "user": user,
        },
    )

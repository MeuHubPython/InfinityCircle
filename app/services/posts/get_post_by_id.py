from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from models.post import Post
from models.user import User
import jwt, os


async def get_post_by_id(post_id: int, request: Request, session: Session):

    post = session.exec(select(Post).where(Post.id == post_id)).one()

    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )
    user = session.exec(select(User).where(User.id == payload["id"])).one()

    return Jinja2Templates(directory="templates").TemplateResponse(
        request=request,
        name="connection_by_id.html",
        context={"post": post, "user": user},
    )

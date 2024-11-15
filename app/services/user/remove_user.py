from sqlmodel import Session, select
from models.user import User
from models.post import Post
from fastapi import Request
from fastapi.responses import RedirectResponse
import jwt, os


async def remove_user(request: Request, session: Session):
    try:
        payload = jwt.decode(
            request.session["Authorization"],
            os.getenv("SECRET_KEY"),
            [os.getenv("ALGORITHM")],
        )

    except jwt.InvalidTokenError:
        return RedirectResponse("/login", status_code=401)

    posts = session.exec(select(Post).where(Post.user_id == payload["id"])).all()
    for post in posts:
        session.delete(post)
    user = session.exec(select(User).where(User.id == payload["id"])).one()
    session.delete(user)
    session.commit()
    del request.session["Authorization"]
    return RedirectResponse("/login", status_code=200)

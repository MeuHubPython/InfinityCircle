from fastapi import Request
from fastapi.responses import RedirectResponse
from schemas.posts.posts import CreatedPost
from sqlmodel import Session, select
from models.post import Post
from models.user import User
from datetime import datetime
import jwt, os


async def create_post(request: Request, new_post: CreatedPost, session: Session):
    payload = jwt.decode(
        request.session["Authorization"],
        os.getenv("SECRET_KEY"),
        algorithms=[os.getenv("ALGORITHM")],
    )

    user = session.exec(select(User).where(User.id == payload["id"])).one()

    post = Post(
        title=new_post.title,
        user_id=user.id,
        body=new_post.body,
        created_at=datetime.now().strftime("%d/%m/%y %H:%M"),
    )

    user.posts.append(post)
    user.posts_count = len(user.posts)

    session.add(post)
    session.add(user)
    session.commit()
    return RedirectResponse("/connections/", status_code=302)

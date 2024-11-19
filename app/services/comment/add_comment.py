from fastapi import Request
from sqlmodel import Session, select
from models.comment import Comment
from models.post import Post
from models.user import User
from fastapi.responses import RedirectResponse
from datetime import datetime
import jwt, os


async def add_comment(request: Request, post_id: int, body: str, session: Session):
    token = request.session["Authorization"]
    payload = jwt.decode(
        token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
    )

    user = session.exec(select(User).where(User.id == payload["id"])).one()

    post = session.exec(select(Post).where(Post.id == post_id)).one()

    comment = Comment(
        user_id=user.id,
        post_id=post_id,
        body=body,
        created_at=datetime.now().strftime("%D %H:%M"),
    )
    post.comments.append(comment)
    post.comments_count = len(post.comments)

    user.comments.append(comment)
    user.comments_count = len(user.comments)

    session.add(comment)
    session.add(user)
    session.add(post)
    session.commit()

    return RedirectResponse(f"/connections/{post_id}", status_code=302)

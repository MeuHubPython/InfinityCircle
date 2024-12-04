from fastapi import Request
from fastapi.responses import RedirectResponse
from schemas.posts.posts import CreatedPost
from sqlmodel import Session, select
from models.post import Post
from models.user import User
from models.mention import Mention
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

    if new_post.mentions:
        try:
            mentioned_user = session.exec(
                select(User).where(User.color == new_post.mentions)
            ).one()
        except Exception:
            return RedirectResponse("/connections/", status_code=404)

        mention = Mention(
            user_id=user.id,
            post_id=new_post.mentions,
            comment_id=None,
            user=mentioned_user,
        )
        mention.post = post

        post.mentions.append(mention)

        user.mentions.append(mention)

        session.add(mention)

    print(user.posts)
    session.add(post)

    user.posts.append(post)
    user.posts_count = len(user.posts)

    session.add(user)
    session.commit()

    return RedirectResponse("/connections/", status_code=302)

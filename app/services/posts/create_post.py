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
        mentions_list = []
        users = new_post.mentions.strip().split(" ")
        print(users)
        for user_mentioned in users:
            try:
                mentioned_user = session.exec(
                    select(User).where(User.color == user_mentioned)
                ).one()
                print("Esse existe: ", mentioned_user.color, mentioned_user.name)

                print(mentioned_user.id)
                mention = Mention(
                    user_id=mentioned_user.id,
                    post_id=post.id,
                    comment_id=None,
                    user=mentioned_user,
                    post=post,
                )
                print(mention.user.id)

                session.add(mention)

                mentions_list.append(mention)

            except Exception:
                print("Esse não existe: ", user_mentioned)
                return RedirectResponse("/connections/", status_code=302)

    session.add(post)

    user.posts.append(post)
    user.posts_count = len(user.posts)

    session.add(user)
    session.commit()

    return RedirectResponse("/connections/", status_code=302)

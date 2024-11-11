from fastapi import Request
from sqlmodel import Session, select
from models.post import Post
from models.user import User
from fastapi.templating import Jinja2Templates
from base64 import b64encode


async def all_posts(request: Request, session: Session):
    post_db = session.exec(select(Post)).all()
    posts = []

    for post in post_db:
        encoded_image = b64encode(
            session.exec(select(User).where(User.id == post.user_id))
            .one()
            .profile_image
        ).decode("utf-8")
        f_image = (
            session.exec(select(User).where(User.id == post.user_id)).one().image_format
        )
        image_uri = "data:" + f_image + ";base64," + encoded_image
        post.profile_image = image_uri
        posts.append(post)

    return Jinja2Templates(directory="templates").TemplateResponse(
        request, "all_posts.html", context={"posts": posts}
    )

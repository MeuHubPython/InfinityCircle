from fastapi import Request
from sqlmodel import Session, select
from models.post import Post
from fastapi.templating import Jinja2Templates


async def all_posts(request: Request, session: Session):
    post_db = session.exec(select(Post)).all()
    posts = []

    for post in post_db:
        posts.append(post)

    return Jinja2Templates(directory="templates").TemplateResponse(
        request, "all_posts.html", context={"posts": posts}
    )

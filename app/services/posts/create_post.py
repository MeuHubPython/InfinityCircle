from fastapi import Request
from schemas.posts.posts import CreatedPost
from sqlmodel import Session
from models.post import Post
import jwt, os


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
        user_name=payload["user"],
    )
    session.add(post)
    session.commit()
    return {"message": "Post created successfully", "post": post}

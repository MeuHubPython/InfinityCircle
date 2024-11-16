from fastapi import APIRouter, Depends, Request, Form
from sqlmodel import Session
from database.init_db import get_session
from schemas.posts.posts import CreatedPost
from services.posts.all_posts import all_posts
from services.posts.create_post import create_post

router = APIRouter(prefix="/posts", tags=["Connections"])


@router.post("/connections")
async def post(
    request: Request,
    title: str = Form(),
    body: str = Form(),
    session: Session = Depends(get_session),
):
    new_post = CreatedPost(title=title, body=body)
    return await create_post(request, new_post, session)


@router.get("/connections")
async def get_all_posts(request: Request, session: Session = Depends(get_session)):
    return await all_posts(request, session)

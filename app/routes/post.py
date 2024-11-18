from fastapi import APIRouter, Depends, Request, Form
from sqlmodel import Session
from database.init_db import get_session
from schemas.posts.posts import CreatedPost
from services.posts.all_posts import all_posts
from services.posts.create_post import create_post
from services.posts.get_post_by_id import get_post_by_id

router = APIRouter(prefix="/connections", tags=["Connections"])


@router.post("/")
async def post(
    request: Request,
    title: str = Form(),
    body: str = Form(),
    session: Session = Depends(get_session),
):
    new_post = CreatedPost(title=title, body=body)
    return await create_post(request, new_post, session)


@router.get("/")
async def get_all_posts(request: Request, session: Session = Depends(get_session)):
    return await all_posts(request, session)


@router.get("/{post_id}")
async def get_post(
    post_id: int, request: Request, session: Session = Depends(get_session)
):
    return await get_post_by_id(post_id, request, session)

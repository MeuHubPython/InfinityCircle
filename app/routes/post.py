from fastapi import APIRouter, Depends, Request, Form
from sqlmodel import Session
from database.init_db import get_session
from schemas.posts.posts import CreatedPost
from services.posts.all_posts import all_posts
from services.posts.create_post import create_post
from services.posts.get_post_by_id import get_post_by_id
from services.flow.add_flow import add_flow
from services.comment.add_comment import add_comment

router = APIRouter(prefix="/connections", tags=["Connections"])


@router.get("/")
async def get_all_posts(request: Request, session: Session = Depends(get_session)):
    return await all_posts(request, session)


@router.get("/{post_id}")
async def get_post(
    post_id: int, request: Request, session: Session = Depends(get_session)
):
    return await get_post_by_id(post_id, request, session)


@router.post("/")
async def post(
    request: Request,
    mentions: str | None = Form(),
    title: str = Form(),
    body: str = Form(),
    session: Session = Depends(get_session),
):
    new_post = CreatedPost(mentions=mentions, title=title, body=body)
    return await create_post(request, new_post, session)


@router.post("/{post_id}/flow")
async def post_flow(
    request: Request, post_id: int, session: Session = Depends(get_session)
):
    return await add_flow(request, post_id, session)


@router.post("/{post_id}/comment")
async def post_comment(
    post_id: int,
    request: Request,
    body: str = Form(),
    session: Session = Depends(get_session),
):
    return await add_comment(request, post_id, body, session)

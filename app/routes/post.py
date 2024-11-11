from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from database.init_db import get_session
from models.post import Post
from schemas.posts.posts import CreatedPost
from services.posts.all_posts import all_posts
from services.posts.create_post import create_post


router = APIRouter(prefix="/posts")


@router.post("/")
async def post(
    request: Request, new_post: CreatedPost, session: Session = Depends(get_session)
):
    return await create_post(request, new_post, session)


@router.get("/all_posts")
async def get_all_posts(request: Request, session: Session = Depends(get_session)):
    return await all_posts(request, session)

from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from schemas.user.user_register import CreateUser
from database.init_db import get_session
from services.user.update_user import update_user
from services.user.remove_user import remove_user
from services.user.me import get_me
from models.user import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all_users")
async def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    all_users = [{user.name: user.email} for user in users]
    return all_users


@router.get("/me")
async def get_user_information(
    request: Request, session: Session = Depends(get_session)
):
    return await get_me(request, session)


@router.put("/update/{user_email}")
async def modify_user(
    user_email: str, modified_user: CreateUser, session: Session = Depends(get_session)
):
    return await update_user(user_email, modified_user, session)


@router.get("/me/delete")
async def delete_user(request: Request, session: Session = Depends(get_session)):
    return await remove_user(request, session)

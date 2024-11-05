from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from schemas.user.user_register import CreateUser
from database.init_db import get_session
from services.user.register_user import register_user
from services.user.update_user import update_user
from services.user.remove_user import remove_user
from models.user import User

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/all_users")
async def get_all_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    all_users = [{user.name: user.email} for user in users]
    return all_users


@router.post("/register")
async def create_user(new_user: CreateUser, session: Session = Depends(get_session)):
    return await register_user(new_user, session)


@router.put("/update/{user_email}")
async def modify_user(
    user_email: str, modified_user: CreateUser, session: Session = Depends(get_session)
):
    return await update_user(user_email, modified_user, session)


@router.delete("/remove/{user.email}")
async def delete_user(user_email: str, session: Session = Depends(get_session)):
    return await remove_user(user_email, session)

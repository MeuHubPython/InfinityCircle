from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
from schemas.user.user_register import CreateUser
from database.init_db import get_session
from services.user.update_user import update_user
from services.user.remove_user import remove_user
from services.user.me import get_me
from services.user.get_card import get_card
from services.user.edit_user import edit_user
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


@router.get("/cards/{user_id}")
async def get_user_cards(
    user_id: int, request: Request, session: Session = Depends(get_session)
):
    return await get_card(user_id, request, session)


@router.get("/me/delete", response_class=HTMLResponse)
async def delete_user(request: Request, session: Session = Depends(get_session)):
    return await remove_user(request, session)


@router.get("/me/edit", response_class=HTMLResponse)
async def update_user(request: Request, session: Session = Depends(get_session)):
    return await edit_user(request, session)


@router.put("/me/edit/submit")
async def modify_user(
    user_email: str, modified_user: CreateUser, session: Session = Depends(get_session)
):
    return await update_user(user_email, modified_user, session)

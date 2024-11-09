from models.user import User
from schemas.user.user_register import CreateUser
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
import bcrypt


async def register_user(request, new_user: CreateUser, session: Session):

    try:
        hashed_password = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt())

        user = User(name=new_user.name, email=new_user.email, password=hashed_password)

        session.add(user)
        session.commit()
        session.refresh(user)

    except Exception:
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request,
            name="register.html",
            context={"email_exists": True},
            status_code=409,
        )

    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
    }

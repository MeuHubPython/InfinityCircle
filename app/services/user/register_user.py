from models.user import User
from schemas.user.user_register import CreateUser
from fastapi import HTTPException
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
        raise HTTPException(status_code=409, detail="Email already in use")

    return {
        "message": "User created successfully",
        "name": user.name,
        "email": user.email,
    }

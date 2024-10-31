from models.user import User
from database.init_db import get_session
from schemas.user import CreateUser
from fastapi import HTTPException
from sqlmodel import Session

async def register_user(new_user: CreateUser, session: Session):
 
    try:
        user = User(
            name=new_user.name,
            email=new_user.email,
            password=new_user.password
        )

        session.add(user)
        session.commit()
        session.refresh(user)

    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")
        
    return {
        "message": "User created successfully",
        "user": user
        
        }
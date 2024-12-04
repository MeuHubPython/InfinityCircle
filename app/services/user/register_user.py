from models.user import User
from schemas.user.user_register import CreateUser
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from datetime import datetime
from base64 import b64encode
from sqlalchemy.exc import IntegrityError
import bcrypt, random

hexadigits = "0123456789abcdef"


def create_user_color():
    user_color = "#"
    for _ in range(6):
        user_color += random.choice(hexadigits)
    user_color += str(random.randint(60, 99))
    return user_color.upper()


async def register_user(
    request, new_user: CreateUser, session: Session, profile_image: bytes | None = None
):
    color = create_user_color()
    try:
        while True:
            try:
                hashed_password = bcrypt.hashpw(
                    new_user.password.encode(), bcrypt.gensalt()
                )
                image = await profile_image.read()
                image_encoded = b64encode(image).decode("utf-8")
                user_image = (
                    "data:" + profile_image.content_type + ";base64," + image_encoded
                )

                user = User(
                    name=new_user.name,
                    color=color,
                    email=new_user.email,
                    password=hashed_password,
                    image_encoded=user_image,
                    created_at=datetime.now().strftime("%d/%m/%y %H:%M"),
                )

                session.add(user)
                session.commit()
                session.refresh(user)
                break

            except IntegrityError:
                color = create_user_color()

    except Exception:
        return Jinja2Templates(directory="templates").TemplateResponse(
            request=request,
            name="register.html",
            context={"email_exists": True},
            status_code=409,
        )

    return RedirectResponse("/login", status_code=302)

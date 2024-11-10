from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
import dotenv, jwt, os

ENV_VARIABLES = dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


ALLOWED_HOSTS = [
    "http://127.0.0.1:8000/login",
    "http://127.0.0.1:8000/login/submit",
    "http://127.0.0.1:8000/register",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8000/static/login.css",
    "http://127.0.0.1:8000/static/index.css",
    "http://127.0.0.1:8000/static/assets/apple-touch-icon.png",
    "http://127.0.0.1:8000/static/assets/favicon-32x32.png",
    "http://127.0.0.1:8000/static/assets/favicon-16x16.png",
    "http://127.0.0.1:8000/static/assets/site.webmanifest",
]


async def create_token(data: dict, request: Request):
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    session_token = request.session["Authorization"] = token
    return session_token


async def authenticate_token(request: Request, call_next):
    if not request.url in ALLOWED_HOSTS:
        token = request.session.get("Authorization")
        if not token:
            return RedirectResponse("/login", status_code=302)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return await call_next(request)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    return await call_next(request)

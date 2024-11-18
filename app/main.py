from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database.init_db import create_table, get_session
from routes.user import router as user_router
from routes.login import router as login_router
from routes.post import router as posts_router
from middlewares.token import authenticate_token
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI()
app.include_router(user_router)
app.include_router(login_router)
app.include_router(posts_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def authentication_middleware(request: Request, call_next):
    return await authenticate_token(request, call_next)


@app.on_event("startup")
async def startup():
    create_table()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), max_age=600)

from models.user import User
from models.post import Post
from sqlmodel import create_engine, Session


DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_table() -> None:
    User.metadata.create_all(bind=engine)
    Post.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session

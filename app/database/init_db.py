from models.user import User
from models.post import Post
from models.comment import Comment
from models.flow import Flow
from models.mention import Mention
from sqlmodel import create_engine, Session


DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_table() -> None:
    User.metadata.create_all(bind=engine)
    Post.metadata.create_all(bind=engine)
    Comment.metadata.create_all(bind=engine)
    Flow.metadata.create_all(bind=engine)
    Mention.metadata.create_all(bind=engine)


def get_session():
    with Session(engine) as session:
        yield session

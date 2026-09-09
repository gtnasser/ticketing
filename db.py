import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///occurrences.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def init_db() -> None:
    Base.metadata.create_all(engine)  # tabelas existentes não são recriadas

def get_user(username: str):
    from models import User
    with SessionLocal() as session:
        return session.scalars(select(User).where(User.username == username)).first()
    
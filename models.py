from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

class Occurrence(Base):
    __tablename__ = "occurrences"

    id: Mapped[int] = mapped_column(primary_key=True)
    occurrence_date: Mapped[str] = mapped_column(String(10), nullable=False)
    occurrence_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    temporary_solution: Mapped[str] = mapped_column(Text, default="")
    definitive_solution: Mapped[str] = mapped_column(Text, default="")
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    registered_at: Mapped[str] = mapped_column(String(19), nullable=False)
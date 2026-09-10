from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy import ForeignKey 
from datetime import datetime
from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True) 
    created_at: Mapped[datetime]
    password_hash: Mapped[str] 
    email: Mapped[str] = mapped_column(unique=True) 


class TaskModel(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str | None]
    completed: Mapped[bool]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))





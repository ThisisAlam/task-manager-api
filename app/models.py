from datetime import date, datetime
from sqlalchemy import (
    Date,
    DateTime,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    mapped_column,
    relationship,
)
class Base(DeclarativeBase):
    pass
class UserModel(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str]= mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    email: Mapped[str]= mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    password: Mapped[str]= mapped_column(
        String(255),
        nullable=False,
    )
    tasks: Mapped["TaskModel"]=relationship(
        back_populates="owner",
    )
class TaskModel(Base):
    __tablename__="tasks"
    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    due_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    estimated_hours: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    owner: Mapped["UserModel"] = relationship(
        back_populates="tasks",
    )
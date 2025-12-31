from datetime import datetime
from typing import List, Optional
import uuid
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import func, ForeignKey


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    username: str = Field(sa_column=Column(mysql.VARCHAR(50), nullable=False))
    email: str = Field(sa_column=Column(mysql.VARCHAR(100), nullable=False, unique=True))
    first_name: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    last_name: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    role: str = Field(sa_column=Column(mysql.VARCHAR(20), nullable=False, server_default="user"))
    is_verified: bool = Field(sa_column=Column(mysql.BOOLEAN, default=False))
    password_hash: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False))
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow))

    books: List["Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Review"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<User {self.username}>"
    


class BookTag(SQLModel, table=True):
    __tablename__ = "book_tags"

    uid: str = Field(
        sa_column=Column(
            mysql.CHAR(36), 
            primary_key=True, 
            default=lambda: str(uuid.uuid4())
        )
    )

    book_id: str = Field(
        sa_column=Column(mysql.CHAR(36), ForeignKey("books.uid"))
    )
    tag_id: str = Field(
        sa_column=Column(mysql.CHAR(36), ForeignKey("tags.uid"))
    )


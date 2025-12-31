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




class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: str = Field(
        sa_column=Column(mysql.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    )
    name: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False))
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, default=datetime.utcnow))

    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    title: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False))
    author: str = Field(sa_column=Column(mysql.VARCHAR(255), nullable=False))
    publisher: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(255), nullable=True))
    published_date: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    page_count: Optional[int] = Field(sa_column=Column(mysql.INTEGER, nullable=True))
    language: Optional[str] = Field(sa_column=Column(mysql.VARCHAR(50), nullable=True))
    user_uid: Optional[str] = Field(sa_column=Column(mysql.CHAR(36), ForeignKey("users.uid")))
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()))

    user: Optional[User] = Relationship(back_populates="books")
    reviews: List["Review"] = Relationship(back_populates="book", sa_relationship_kwargs={"lazy": "selectin"})
    tags: List[Tag] = Relationship(link_model=BookTag, back_populates="books", sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: str = Field(
        sa_column=Column(
            mysql.CHAR(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: str(uuid.uuid4())
        )
    )
    rating: int = Field(sa_column=Column(mysql.TINYINT, nullable=False))
    review_text: str = Field(sa_column=Column(mysql.VARCHAR(1000), nullable=False))
    user_uid: Optional[str] = Field(sa_column=Column(mysql.CHAR(36), ForeignKey("users.uid")))
    book_uid: Optional[str] = Field(sa_column=Column(mysql.CHAR(36), ForeignKey("books.uid")))
    created_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, server_default=func.now()))
    updated_at: datetime = Field(sa_column=Column(mysql.DATETIME, nullable=False, server_default=func.now(), onupdate=func.now()))

    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"


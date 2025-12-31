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
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "publisher": "Scribner",
                "published_date": "1925-04-10",
                "page_count": 218,
                "language": "English"
            }
        }
    }


class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "publisher": "Scribner",
                "page_count": 218,
                "language": "English"
            }
        }
    }



class BookReadModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "publisher": "Scribner",
                "published_date": "1925-04-10T00:00:00",
                "page_count": 218,
                "language": "English",
                "created_at": "2025-11-09T12:00:00",
                "updated_at": "2025-11-09T12:00:00"
            }
        }
    }

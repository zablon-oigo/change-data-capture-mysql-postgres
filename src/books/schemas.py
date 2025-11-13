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

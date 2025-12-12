import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ReviewModel(BaseModel):
    uid: uuid.UUID
    rating: int = Field(..., le=5, description="Rating for the book, max value 5")
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True, 
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "rating": 5,
                "review_text": "Highly recommend it.",
                "user_uid": "987e6543-e21b-12d3-a456-426614174111",
                "book_uid": "555e4444-e21b-12d3-a456-426614174222",
                "created_at": "2025-11-09T12:00:00",
                "updated_at": "2025-11-09T12:00:00"
            }
        }
    }


class ReviewCreateModel(BaseModel):
    rating: int = Field(..., le=5, description="Rating for the book, max value 5")
    review_text: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "rating": 4,
                "review_text": "Really enjoyed this book!"
            }
        }
    }

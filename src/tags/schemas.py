import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TagModel(BaseModel):
    uid: uuid.UUID
    name: str
    created_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "uid": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Fiction",
                "created_at": "2025-11-09T12:00:00"
            }
        }
    }



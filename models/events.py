from pydantic import BaseModel, Field
from typing import List


class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str] = Field(default_factory=list)
    location: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch",
                "image": "https://example.com/image.png",
                "description": "Presentation of a new book about FastAPI",
                "tags": ["python", "fastapi", "book"],
                "location": "Google Meet"
            }
        }
    }

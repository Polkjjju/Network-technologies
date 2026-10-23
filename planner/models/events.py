from pydantic import BaseModel, Field, ConfigDict


class Event(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch",
                "image": "https://example.com/image.png",
                "description": "Презентация проекта FastAPI",
                "tags": ["python", "fastapi", "book"],
                "location": "Google Meet"
            }
        }
    )

    id: int
    title: str
    image: str
    description: str
    tags: list[str] = Field(default_factory=list)
    location: str

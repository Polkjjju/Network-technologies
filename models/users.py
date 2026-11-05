from pydantic import BaseModel, EmailStr, Field
from typing import List

from models.events import Event


class User(BaseModel):
    email: EmailStr
    events: List[Event] = Field(default_factory=list)


class NewUser(User):
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "password": "Stro0ng!",
                "events": []
            }
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "password": "Stro0ng!"
            }
        }
    }

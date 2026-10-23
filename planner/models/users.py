from pydantic import BaseModel, EmailStr, Field

from models.events import Event


class User(BaseModel):
    email: EmailStr
    username: str
    events: list[Event] = Field(default_factory=list)


class NewUser(User):
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

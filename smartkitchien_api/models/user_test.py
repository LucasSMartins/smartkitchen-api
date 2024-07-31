from typing import Optional

from beanie import Document
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None


class UserModel(Document, User):
    class Settings:
        collection = 'users'

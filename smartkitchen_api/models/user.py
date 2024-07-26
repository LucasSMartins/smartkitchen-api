from datetime import datetime
from re import search as re_search

from beanie import Document
from pwdlib import PasswordHash
from pydantic import EmailStr, Field, field_validator

pwd_context = PasswordHash.recommended()


class User(Document):
    username: str = Field(..., min_length=5, max_length=15)
    email: EmailStr
    password: str = Field(..., min_length=8)
    created_at: datetime = Field(default_factory=lambda: datetime.now().isoformat())

    @field_validator('email')
    def lowercase_email(cls, value: EmailStr) -> EmailStr:
        return value.lower()

    @field_validator('password')
    def validate_password(cls, password_value):
        if not re_search(r'[A-Z]', password_value):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not re_search(r'[a-z]', password_value):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        if not re_search(r'[!@#$%^&*(),.?":{}|<> ]', password_value):
            raise ValueError('A senha deve conter pelo menos um caractere especial')
        if not re_search(r'[0-9]', password_value):
            raise ValueError('A senha deve conter pelo menos um número')

        return pwd_context.hash(password_value)

    class Settings:
        name = 'users'


# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)
# https://polar.sh/frankie567/posts/introducing-pwdlib-a-modern-password-hash-helper-for-python


class UpdateUser(User):
    username: str | None = None
    email: EmailStr | None = None
    password: datetime | None = None

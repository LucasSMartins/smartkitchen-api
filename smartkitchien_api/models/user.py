from datetime import datetime
from re import match as re_match
from re import search as re_search

from beanie import Document
from pwdlib import PasswordHash
from pydantic import BaseModel, EmailStr, Field, field_validator

pwd_context = PasswordHash.recommended()


class User(Document):
    username: str = Field(..., min_length=3, max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=8)
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('username')
    def validade_username(cls, username_value: str):
        if not re_match(r'^[a-zA-Z0-9._]+$', username_value):
            raise ValueError(
                'O nome de usuário deve conter apenas letras,números,  underline ou ponto.'  # noqa: E501
            )

        if re_search(r'(.)\1{3,}', username_value):
            raise ValueError(
                'O nome de usuário não deve conter repetição excessiva de caracteres'
            )

        return username_value

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


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=15)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8)

    @field_validator('username')
    def validade_username(cls, username_value: str):
        if not re_match(r'^[a-zA-Z0-9._]+$', username_value):
            raise ValueError(
                'O nome de usuário deve conter apenas letras,números, underline ou ponto.'  # noqa: E501
            )

        if re_search(r'(.)\1{3,}', username_value):
            raise ValueError(
                'O nome de usuário não deve conter repetição excessiva de caracteres'
            )

        return username_value

    @field_validator('email')
    def lowercase_email(cls, value: EmailStr):
        return value.lower()

    @field_validator('password')
    def validate_password(cls, password_value):
        if not re_search(r'[A-Z]', password_value):
            raise ValueError('A senha deve conter pelo menos uma letra maiúscula')
        if not re_search(r'[a-z]', password_value):
            raise ValueError('A senha deve conter pelo menos uma letra minúscula')
        if not re_search(r'[!@#$%^&*(),.?":{}|<>]', password_value):
            raise ValueError('A senha deve conter pelo menos um caractere especial')
        if not re_search(r'[0-9]', password_value):
            raise ValueError('A senha deve conter pelo menos um número')

        return pwd_context.hash(password_value)


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    created_at: str | datetime

    @field_validator('created_at')
    def datetime_to_human_readable(cls, created_at_value):
        if isinstance(created_at_value, datetime):
            return created_at_value.strftime('%d/%m/%Y %H:%M:%S')
        raise ValueError('Data/hora fornecida está em formato inválido')


user_example = {
    'username': 'usertest',
    'email': 'usertest@example.com',
    'password': 'myS&cret007',
}

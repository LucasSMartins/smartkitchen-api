from typing import Optional

import pytest
from beanie import Document, init_beanie
from mongomock_motor import AsyncMongoMockClient
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    age: Optional[int] = None


class UserModel(Document, User):
    class Settings:
        collection = 'users'


@pytest.fixture(autouse=True)
async def my_fixture():
    client = AsyncMongoMockClient()
    # Inicializa o Beanie com o cliente MongoMock
    await init_beanie(
        document_models=[UserModel], database=client.get_database(name='db')
    )

    return client


@pytest.mark.asyncio()
async def test_create_user():
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[UserModel], database=client.get_database(name='db')
    )

    # Cria um usuário
    new_user = UserModel(username='test_user', email='test@example.com', age=30)
    await new_user.insert()

    # Recupera o usuário do banco de dados
    user = await UserModel.find_one(UserModel.username == 'test_user')

    AGE = 30

    # Verifica se o usuário foi inserido corretamente
    assert user is not None
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.age == AGE

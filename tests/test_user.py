import pytest
from beanie import init_beanie
from models import UserModel
from mongomock_motor import AsyncMongoMockClient

from smartkitchien_api.models.user_test import UserTest


@pytest.mark.asyncio()
async def test_create_user():
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=[UserTest], database=client.get_database(name='db')
    )

    # Cria um usuário
    new_user = UserTest(username='test_user', email='test@example.com', age=30)
    await new_user.insert()

    # Recupera o usuário do banco de dados
    user = await UserModel.find_one(UserTest.username == 'test_user')

    AGE = 30

    # Verifica se o usuário foi inserido corretamente
    assert user is not None
    assert user.username == 'test_user'
    assert user.email == 'test@example.com'
    assert user.age == AGE

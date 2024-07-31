import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from smartkitchien_api.models.user_test import UserTest


@pytest.fixture(autouse=True)
async def my_fixture():
    client = AsyncMongoMockClient()
    # Inicializa o Beanie com o cliente MongoMock
    await init_beanie(
        document_models=[UserTest], database=client.get_database(name='db')
    )
    # Use 'yield' em vez de 'return'
    # para garantir que o fixture seja aguardado.
    return client

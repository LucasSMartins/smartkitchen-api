import pytest_asyncio  # type: ignore
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient  # type: ignore

from smartkitchien_api.models.user import User


@pytest_asyncio.fixture(autouse=True)
async def init_mongo():
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[User], database=client.get_database(name='db'))

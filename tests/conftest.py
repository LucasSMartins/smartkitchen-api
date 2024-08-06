import pytest
import pytest_asyncio  # type: ignore
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient  # type: ignore

from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import create_access_token, get_password_hash


@pytest_asyncio.fixture(autouse=True)
async def init_mongo():
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[User], database=client.get_database(name='db'))


@pytest_asyncio.fixture()
async def test_current_user():
    pwd_hash = get_password_hash('myS&cret007')
    current_user = User(
        username='usertest',
        email='usertest@example.com',
        password=pwd_hash,
    )

    await current_user.save()

    return current_user


@pytest.fixture()
def token(test_current_user):
    token = create_access_token({'sub': test_current_user.username})
    return {'Authorization': f'Bearer {token}'}

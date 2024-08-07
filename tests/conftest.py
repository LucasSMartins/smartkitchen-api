import pytest_asyncio  # type: ignore
from beanie import init_beanie
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient  # type: ignore

from smartkitchien_api.main import app
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_password_hash

# from smartkitchien_api.security.security import get_password_hash

# from smartkitchien_api.security.security import create_access_token


@pytest_asyncio.fixture(autouse=True)
async def init_mongo():
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[User], database=client.get_database(name='db'))


@pytest_asyncio.fixture
async def client():
    client = TestClient(app=app)
    return client


@pytest_asyncio.fixture()
async def faker_user():
    faker_user_data = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': get_password_hash('myS&cret007'),
    }

    await User(**faker_user_data).insert()

    faker_user_db = await User.find(
        User.username == faker_user_data['username']
    ).first_or_none()

    return faker_user_db


@pytest_asyncio.fixture()
async def another_faker_user():
    faker_user_data = {
        'username': 'usertest2',
        'email': 'usertest2@example.com',
        'password': get_password_hash('myS&cret007'),
    }

    await User(**faker_user_data).insert()

    faker_user_db = await User.find(
        User.username == faker_user_data['username']
    ).first_or_none()

    return faker_user_db


@pytest_asyncio.fixture()
def token(client, faker_user):
    response = client.post(
        '/api/token',
        data={'username': faker_user.username, 'password': 'myS&cret007'},
    )

    return response.json()['access_token']  # type: ignore

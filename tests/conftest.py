import pytest_asyncio
from beanie import init_beanie
from fastapi.testclient import TestClient
from mongomock_motor import AsyncMongoMockClient

from smartkitchien_api.main import app
from smartkitchien_api.models.cookbook import Cookbook
from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.faker_user import FakerUser
from smartkitchien_api.security.security import get_password_hash

list_document_models = [User, Cookbook, Pantry]


@pytest_asyncio.fixture(autouse=True)
async def init_mongo():
    client = AsyncMongoMockClient()
    await init_beanie(
        document_models=list_document_models, database=client.get_database(name='db')
    )


@pytest_asyncio.fixture
async def client():
    # client = TestClient(app=app, base_url='/api')
    client = TestClient(app=app)
    return client


@pytest_asyncio.fixture()
async def faker_user():
    faker_user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': get_password_hash('myS&cret007'),
        'clean_password': 'myS&cret007',
    }

    await FakerUser(**faker_user_data).insert()

    faker_user_db = await FakerUser.find(
        FakerUser.username == faker_user_data['username']
    ).first_or_none()

    return faker_user_db


@pytest_asyncio.fixture()
async def another_faker_user():
    another_faker_user_data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': get_password_hash('myS&cret007'),
        'clean_password': 'myS&cret007',
    }

    await FakerUser(**another_faker_user_data).insert()

    another_faker_user_db = await FakerUser.find(
        FakerUser.username == another_faker_user_data['username']
    ).first_or_none()

    return another_faker_user_db


@pytest_asyncio.fixture()
async def token(client: TestClient, faker_user: FakerUser):
    response = client.post(
        '/api/token',
        data={'username': faker_user.username, 'password': faker_user.clean_password},
    )

    return response.json()['access_token']


@pytest_asyncio.fixture()
async def headers(token):
    return {'Authorization': f'Bearer {token}'}


@pytest_asyncio.fixture()
async def user_pantry(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    category_value = '101'
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    client.post(
        f'/api/pantry/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    return pantry


@pytest_asyncio.fixture()
async def user_cookbook(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    category_value = '101'

    # Fazer a requisição POST para criar uma receita
    client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    return cookbook

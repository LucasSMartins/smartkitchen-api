from datetime import datetime, timedelta

import pytest
from bson import ObjectId
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchen_api.models.user import User
from smartkitchen_api.schema.faker_user import FakerUser
from smartkitchen_api.security.security import verify_password


@pytest.mark.asyncio()
async def test_create_user_returns_201_when_successful(client: TestClient):
    # Teste para criação de usuário válido
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_201_CREATED

    # Verifique se o usuário foi criado com sucesso
    user = await User.find_one(User.email == new_user['email'])

    assert user is not None
    assert user.username == new_user['username']
    assert user.email == new_user['email']
    assert isinstance(user.created_at, datetime)

    # Verifique se o campo created_at está dentro de um intervalo de tempo razoável
    current_time = datetime.now()
    time_interval = timedelta(seconds=1)
    assert current_time - time_interval < user.created_at < current_time + time_interval

    assert verify_password(
        plain_password=new_user['password'], hashed_password=user.password
    )

    assert ObjectId.is_valid(user.id)


# @ =============== TESTES DE ERROR =================
@pytest.mark.asyncio()
async def test_create_user_returns_409_when_username_exists(
    client: TestClient, faker_user: FakerUser
):
    # Teste para falha ao criar usuário com nome de usuário existente
    new_user = {
        'username': 'testuser',
        'email': 'user_test@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_username_missing(client: TestClient):
    # Teste para falha ao criar usuário sem nome de usuário
    new_user = {
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_username_too_short(client: TestClient):
    # Teste para falha ao criar usuário com nome de usuário menor que 3 caracteres
    new_user = {
        'username': 'us',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_username_too_long(client: TestClient):
    # Teste para falha ao criar usuário com nome de usuário maior que 16 caracteres

    new_user = {
        'username': 'testuser_testuser_testuser_testuser',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_username_contains_special_chars(
    client: TestClient,
):
    # Teste para falha ao criar usuário com nome de usuário
    # contendo caracteres especiais

    new_user = {
        'username': 'testuser#',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_username_contains_repeated_chars(
    client: TestClient,
):
    # Teste para falha ao criar usuário com mais de 3 caracteres
    # repetidos no nome de usuário
    new_user = {
        'username': 'uuuutestuser',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchen_api.models.user import User


@pytest.mark.asyncio()
async def test_create_user_returns_409_when_email_already_exists(client: TestClient):
    new_user = {
        'username': 'testuser_email',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    # Crie um usuário existente
    await User(
        username='testuser', email='testuser@example.com', password='myS&cret007'
    ).create()

    # Faça uma requisição POST para a rota de criação de usuário
    response = client.post('/api/users', json=new_user)

    # Verifique se a requisição foi bem-sucedida
    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_is_missing(client: TestClient):
    new_user = {
        'username': 'testuser',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_lacks_at_sign(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuserexample.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_contains_space(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser @example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_has_invalid_character(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example!.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_has_no_domain(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_has_invalid_domain(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.invalid',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_has_multiple_at_signs(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_email_contains_non_allowed_character(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com£',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

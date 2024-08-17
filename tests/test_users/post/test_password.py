import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_is_missing(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_is_too_short(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'my',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_missing_uppercase(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'mysecret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_missing_lowercase(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'MYS&CRET007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_missing_special_character(
    client: TestClient,
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'mySecret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_user_returns_422_when_password_missing_number(client: TestClient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'myS&cret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

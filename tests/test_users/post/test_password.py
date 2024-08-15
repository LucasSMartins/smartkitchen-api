import pytest
from fastapi import status
from fastapi.testclient import TestClient

@pytest.mark.asyncio()
async def test_required_field_password(client: Testclient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



@pytest.mark.asyncio()
async def test_password_validation_lt_8(client: Testclient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'my',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



@pytest.mark.asyncio()
async def test_password_validation_must_contain_character_uppercase(
    client: Testclient
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'mysecret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_password_validate_password_must_contain_least_one_lowercase_letter(
    client: TestClient
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'MYS&CRET007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_password_validation_must_contain_special_character(
    client: Testclient
):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'mySecret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_password_validation_must_contain_number(client: Testclient):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'myS&cret',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

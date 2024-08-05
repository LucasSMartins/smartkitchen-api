import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.main import app

# Crie um cliente de teste para a aplicação FastAPI
client = TestClient(app)


@pytest.mark.asyncio()
async def test_required_field_password():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_lt_8():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'my',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'string_too_short'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_character_uppercase():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'mysecret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_special_character():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'mySecret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_number():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'myS&cret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']

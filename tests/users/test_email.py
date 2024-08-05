import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.main import app
from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.user import User

# Crie um cliente de teste para a aplicação FastAPI
client = TestClient(app)


@pytest.mark.asyncio()
async def test_email_exist():
    new_user = {
        'username': 'usertest_email',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    # Crie um usuário existente
    await User(
        username='usertest', email='usertest@example.com', password='myS&cret007'
    ).create()

    # Faça uma requisição POST para a rota de criação de usuário
    response = client.post('/api/users', json=new_user)

    # Verifique se a requisição foi bem-sucedida
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': ErrorMessages.EMAIL_ALREADY_EXISTS}


@pytest.mark.asyncio()
async def test_required_field_email():
    new_user = {
        'username': 'usertest',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation():
    new_user = {
        'username': 'usertest',
        'email': 'usertestexample.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_space():
    new_user = {
        'username': 'usertest',
        'email': 'usertest @example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_invalid_character():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example!.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_without_domain():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_invalid_domain():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.invalid',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_multiple_at():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_non_allowed_character():
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com£',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']

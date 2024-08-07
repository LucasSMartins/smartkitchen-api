import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.user import User


@pytest.mark.asyncio()
async def test_email_exist(client):
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
async def test_required_field_email(client):
    new_user = {
        'username': 'usertest',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_without_at_sign(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertestexample.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_space(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest @example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_invalid_character(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example!.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)  # type: ignore

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_without_domain(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_invalid_domain(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.invalid',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_multiple_at(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']


@pytest.mark.asyncio()
async def test_email_validation_with_non_allowed_character(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com£',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'email']

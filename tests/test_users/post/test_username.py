from datetime import datetime, timedelta

import pytest
from bson import ObjectId
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import verify_password


# Crie um teste para a rota de criação de usuário
@pytest.mark.asyncio()
async def test_create_user(client):
    # Crie um novo usuário
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    # Faça uma requisição POST para a rota de criação de usuário
    response = client.post('/api/users', json=new_user)

    # Verifique se a requisição foi bem-sucedida
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.USER_CREATED}  # type: ignore

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


@pytest.mark.asyncio()
async def test_username_exist(client):
    new_user = {
        'username': 'usertest',
        'email': 'user_test@example.com',
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
    assert response.json() == {'detail': ErrorMessages.USERNAME_ALREADY_EXISTS_409}  # type: ignore


@pytest.mark.asyncio()
async def test_required_field_username(client):
    new_user = {
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'username']


@pytest.mark.asyncio()
async def test_username_validation_lt_3_characters(client):
    new_user = {
        'username': 'us',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'string_too_short'
    assert msg['loc'] == ['body', 'username']


@pytest.mark.asyncio()
async def test_username_validation_gt_16_characters(client):
    new_user = {
        'username': 'usertest_usertest_usertest_usertest',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'string_too_long'
    assert msg['loc'] == ['body', 'username']


@pytest.mark.asyncio()
async def test_username_validation_must_not_contain_special_characters(client):
    new_user = {
        'username': 'usertest#',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'username']


@pytest.mark.asyncio()
async def test_username_validation_must_not_contain_more_3_repeated_characters_sequence(
    client,
):  # noqa: E501
    new_user = {
        'username': 'uuuuusertest',
        'email': 'usertest@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'username']

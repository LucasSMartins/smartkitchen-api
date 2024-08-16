from datetime import timedelta

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from freezegun import freeze_time

from smartkitchien_api.schema.faker_user import FakerUser
from smartkitchien_api.schema.token import Token
from smartkitchien_api.security.security import (
    create_access_token,
    get_current_user,
    validate_jwt,
)


@pytest.mark.asyncio()
async def test_get_token(client: TestClient, faker_user: FakerUser):
    response = client.post(
        '/api/token',
        data={'username': faker_user.username, 'password': faker_user.clean_password},
    )

    token = response.json()['access_token']
    token_type = response.json()['token_type']

    assert response.status_code == status.HTTP_201_CREATED
    assert token is not None
    assert token_type == 'bearer'
    assert validate_jwt(token)


@pytest.mark.asyncio()
async def test_get_token_username_or_email_invalid(client):
    response = client.post(
        '/api/token',
        data={'username': 'testuser_abcde', 'password': 'myS&cret007_12345'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_expired_after_time(client: TestClient, faker_user: FakerUser):
    # Cria o usuário em um determinado tempo.
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/api/token',
            data={
                'username': faker_user.username,
                'password': faker_user.clean_password,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        token_that_will_expire = response.json()['access_token']

    # Tenta acessar uma rota em que o token já está expirado.
    with freeze_time('2023-07-14 12:31:00'):
        response = client.get(
            f'/api/users/{faker_user.id}',
            headers={'Authorization': f'Bearer {token_that_will_expire}'},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_current_user_valid_token(token):
    current_user = await get_current_user(token)

    assert current_user.username == 'testuser'


@pytest.mark.asyncio()
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as http_exc:
        await get_current_user('invalid_token')

    assert http_exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_current_user_invalid_username():
    # Cria um token sem o payload sub.
    access_token = create_access_token(payload_data={})

    token = Token(access_token=access_token, token_type='bearer')

    with pytest.raises(HTTPException) as http_exc:
        await get_current_user(token)

    assert http_exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_current_user_already_existing_username():
    # Cria um token sem o payload sub.
    access_token = create_access_token(payload_data={'sub': 'non_existing_testuser'})

    token = Token(access_token=access_token, token_type='bearer')

    with pytest.raises(HTTPException) as http_exc:
        await get_current_user(token)

    assert http_exc.value.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_create_access_token(faker_user):
    access_token = create_access_token(
        payload_data={'sub': faker_user.username},
        expires_delta=timedelta(minutes=30),
    )

    assert access_token


@pytest.mark.asyncio()
async def test_validate_jwt_invalid(faker_user):
    is_valid_jwt = validate_jwt('token_invalid')

    assert not is_valid_jwt

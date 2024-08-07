import pytest
from fastapi import status

from smartkitchien_api.security.security import validate_jwt


# TODO: Criar um Schema que herda o User mas com o campo
# senha em claro para usar nesta rota e na fixture token em confest.
@pytest.mark.asyncio()
async def test_get_token(client, faker_user):
    response = client.post(
        '/api/token',
        data={'username': faker_user.username, 'password': 'myS&cret007'},
    )

    token = response.json()['access_token']  # type: ignore
    token_type = response.json()['token_type']  # type: ignore

    assert response.status_code == status.HTTP_201_CREATED
    assert token is not None
    assert token_type == 'bearer'
    assert validate_jwt(token)


@pytest.mark.asyncio()
async def test_get_token_username_or_email_invalid(client):
    response = client.post(
        '/api/token',
        data={'username': 'usertest_abcde', 'password': 'myS&cret007_12345'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['detail'] == 'O email ou senha estão incorretos'  # type: ignore

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.main import app
from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_password_hash

# Crie um cliente de teste para a aplicação FastAPI
client = TestClient(app)


@pytest.mark.asyncio()
async def test_read_all_users_and_returns_list_users():
    pwd_hash = get_password_hash('myS&cret007')
    users = [
        User(username='usertest1', email='usertest1@example.com', password=pwd_hash),
        User(
            username='usertest2',
            email='usertest2@example.com',
            password=pwd_hash,
        ),
    ]

    for user in users:
        await user.save()

    response = client.get('/api/users')

    user_response = User(**response.json()[0])

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(user_response, User)


@pytest.mark.asyncio()
async def test_read_all_users_and_empty_returns_not_found():
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == ErrorMessages.USER_NOT_FOUND


@pytest.mark.asyncio()
async def test_read_user_me(test_current_user, token):
    response = client.get('/api/users/me', headers=token)
    assert response.status_code == status.HTTP_200_OK

    assert response.json()['username'] == test_current_user.username
    assert response.json()['email'] == test_current_user.email

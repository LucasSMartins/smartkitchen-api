import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_password_hash


@pytest.mark.asyncio()
async def test_read_all_users_and_returns_list_users(client):
    pwd_hash = get_password_hash('myS&cret007')
    users = [
        User(username='testuser1', email='testuser1@example.com', password=pwd_hash),
        User(
            username='testuser2',
            email='testuser2@example.com',
            password=pwd_hash,
        ),
    ]

    for user in users:
        await user.save()

    response = client.get('/api/users')

    user_response = User(**response.json()[0])  # type: ignore

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert isinstance(user_response, User)


@pytest.mark.asyncio()
async def test_read_all_users_and_empty_returns_not_found(client):
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == ErrorMessages.USER_NOT_FOUND  # type: ignore


@pytest.mark.asyncio()
async def test_read_user_me(client, token, faker_user):
    response = client.get('/api/users/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == status.HTTP_200_OK

    assert response.json()['username'] == faker_user.username  # type: ignore
    assert response.json()['email'] == faker_user.email  # type: ignore


@pytest.mark.asyncio()
async def test_read_user_and_return_user_by_id(client, token, faker_user):
    response = client.get(
        f'/api/users/{faker_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == faker_user.username  # type: ignore
    assert response.json()['email'] == faker_user.email  # type: ignore

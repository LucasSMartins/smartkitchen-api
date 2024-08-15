import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_password_hash


@pytest.mark.asyncio()
async def test_read_all_users_and_returns_list_users(
    client: TestClient, faker_user: FakerUser, another_faker_user: FakerUser
):
    
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_200_OK
   


@pytest.mark.asyncio()
async def test_read_all_users_and_empty_returns_not_found(client):
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_read_user_me(
    client: TestClient, faker_user: FakerUser, headers: dict
):
    response = client.get('/api/users/me', headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_read_user_and_return_user_by_id(
    client: TestClient, faker_user: FakerUser, headers: dict
):
    response = client.get(
        f'/api/users/{faker_user.id}', headers=headers
    )

    assert response.status_code == status.HTTP_200_OK


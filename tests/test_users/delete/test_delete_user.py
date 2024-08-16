import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_delete_faker_user(
    client: TestClient, faker_user: FakerUser, headers: dict
):
    response = client.delete(f'/api/users/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_delete_another_faker_user(
    client: TestClient, another_faker_user: FakerUser, headers: dict
):
    response = client.delete(
        f'/api/users/{another_faker_user.id}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_delete_faker_user_unauthenticated(
    client: TestClient, faker_user: FakerUser
):
    response = client.delete(f'/api/users/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_with_user_id_invalid(client: TestClient, headers: dict):
    response = client.delete('/api/users/999999', headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_non_existent_user(client: TestClient, headers: dict):
    user_id_not_existing = '5eb7cf5a86d9755df3a6c593'

    response = client.delete(f'/api/users/{user_id_not_existing}', headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_delete_user_with_invalid_token(
    client: TestClient, faker_user: FakerUser
):
    response = client.delete(
        f'/api/users/{faker_user.id}', headers={'Authorization': 'Bearer invalid_token'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

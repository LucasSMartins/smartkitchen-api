import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.cookbook import Cookbook
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    response = client.get(
        f'/api/cookbook/{faker_user.id}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_404_when_cookbook_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    response = client.get(f'/api/cookbook/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_400_when_user_id_is_invalid(
    client: TestClient,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    user_id = '5eb7cf5a86d9755df3a6c593'

    response = client.get(f'/api/cookbook/{user_id}', headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_401_when_unauthenticated(
    client: TestClient,
    faker_user: FakerUser,
):
    response = client.get(f'/api/cookbook/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_401_when_invalid_token(
    client: TestClient,
    faker_user: FakerUser,
):
    headers = {'Authorization': 'Bearer invalid_token'}

    response = client.get(f'/api/cookbook/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_read_user_cookbook_returns_422_when_user_id_is_invalid(
    client: TestClient,
    headers: dict[str, str],
):
    user_id = 'invalid_user_id'

    response = client.get(f'/api/cookbook/{user_id}', headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_get_user_pantry_returns_200_when_authenticated(
    client: TestClient, faker_user: User, headers: dict[str, str], user_pantry: Pantry
):
    response = client.get(f'/api/pantry/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK

    # pantry = response.json().get('detail')
    # assert isinstance(pantry, dict)
    # assert isinstance(pantry['pantry'], list)
    # assert len(pantry['pantry']) >= 1
    # pantry_public = PantryPublic(**pantry)
    # assert isinstance(pantry_public, PantryPublic)


@pytest.mark.asyncio()
async def test_get_user_pantry_returns_401_when_token_is_missing(
    client: TestClient, faker_user: FakerUser
):
    response = client.get(f'/api/pantry/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_user_pantry_returns_401_when_token_is_invalid(
    client: TestClient, faker_user: FakerUser
):
    response = client.get(
        f'/api/pantry/{faker_user.id}',
        headers={'Authorization': 'Bearer token_invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_user_pantry_returns_400_when_user_id_does_not_exist(
    client: TestClient, headers: dict[str, str]
):
    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    response = client.get(f'/api/pantry/{non_existent_user_id}', headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_get_user_pantry_returns_422_when_user_id_is_invalid(
    client: TestClient, headers: dict[str, str]
):
    invalid_user_id = '9999'

    response = client.get(f'/api/pantry/{invalid_user_id}', headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

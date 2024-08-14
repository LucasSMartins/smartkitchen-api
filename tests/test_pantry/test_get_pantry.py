import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.models.pantry import PantryPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_get_user_pantry(
    client: TestClient, faker_user: User, headers: dict, create_pantry
):
    response = client.get(f'/api/pantry/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.json()

    pantry = response.json().get('detail')

    assert isinstance(pantry, dict)
    assert isinstance(pantry['pantry'], list)
    assert len(pantry['pantry']) >= 1

    pantry_public = PantryPublic(**pantry)
    assert isinstance(pantry_public, PantryPublic)


# @ ============== TESTES DE ERROR ===============


@pytest.mark.asyncio()
async def test_get_user_pantry_without_token(client: TestClient, faker_user: FakerUser):
    response = client.get(f'/api/pantry/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.NOT_AUTHENTICATED_401


@pytest.mark.asyncio()
async def test_get_user_pantry_with_invalid_token(
    client: TestClient, faker_user: FakerUser
):
    response = client.get(
        f'/api/pantry/{faker_user.id}',
        headers={'Authorization': 'Bearer token_invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.NOT_VALIDATE_CREDENTIALS_401


@pytest.mark.asyncio()
async def test_get_user_pantry_with_nonexistent_user(client: TestClient, headers: dict):
    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    response = client.get(f'/api/pantry/{non_existent_user_id}', headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.json()


@pytest.mark.asyncio()
async def test_get_user_pantry_with_user_id_invalid(client: TestClient, headers: dict):
    invalid_user_id = '9999'

    response = client.get(f'/api/pantry/{invalid_user_id}', headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'detail' in response.json()
    assert response.json()['detail']['type'] == 'value_error'
    assert response.json()['detail']['loc'] == ['path', 'user_id']

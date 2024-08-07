import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages


@pytest.mark.asyncio()
async def test_delete_faker_user(client, faker_user, token):
    response = client.delete(
        f'/api/users/{faker_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': SuccessMessages.USER_DELETED}


@pytest.mark.asyncio()
async def test_delete_another_faker_user(client, another_faker_user, token):
    response = client.delete(
        f'/api/users/{another_faker_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        'detail': ErrorMessages.BAD_REQUEST_CHECK_PERMISSION_USER
    }


@pytest.mark.asyncio()
async def test_delete_faker_user_unauthenticated(client, faker_user):
    response = client.delete(f'/api/users/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.UNAUTHORIZED}


@pytest.mark.asyncio()
async def test_delete_with_user_id_invalid(client, token):
    response = client.delete(
        '/api/users/999999', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == ErrorMessages.VALUE_ERROR  # type: ignore
    assert response.json()['detail'][0]['msg'] == ErrorMessages.PYDANTIC_OBJECT_ID  # type: ignore


@pytest.mark.asyncio()
async def test_delete_non_existent_user(client, token):
    response = client.delete(
        '/api/users/5eb7cf5a86d9755df3a6c593',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == ErrorMessages.BAD_REQUEST_CHECK_PERMISSION_USER  # type: ignore


@pytest.mark.asyncio()
async def test_delete_user_with_invalid_token(client, faker_user):
    response = client.delete(
        f'/api/users/{faker_user.id}', headers={'Authorization': 'Bearer invalid_token'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.TOKEN_INVALID}

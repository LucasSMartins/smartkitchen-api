import pytest
from fastapi import status

from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_password_hash, verify_password


@pytest.mark.asyncio()
async def test_update_username_using_just_username(client, faker_user, token):
    update_faker_user = {'username': 'new_usertest'}
    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.json()
    assert response.json()['detail']['username'] != faker_user.username  # type: ignore
    assert response.json()['detail']['username'] == update_faker_user['username']  # type: ignore


@pytest.mark.asyncio()
async def test_update_email_using_just_email(client, faker_user, token):
    update_faker_user = {'email': 'new_usertest@example.com'}
    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.json()
    assert response.json()['detail']['email'] == update_faker_user['email']  # type: ignore


@pytest.mark.asyncio()
async def test_update_password_using_just_password(client, faker_user, token):
    update_faker_user = {'password': 'newmyS&cret007'}

    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    # Buscar o usuário no banco de dados após a atualização
    updated_user = await User.get(faker_user.id)

    passwords_match = verify_password(
        plain_password=update_faker_user['password'],
        hashed_password=updated_user.password,
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.json()
    assert passwords_match

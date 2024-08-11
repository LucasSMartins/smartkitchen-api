import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import verify_password


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
    assert response.json()['detail'] == SuccessMessages.UPDATE_USER  # type: ignore


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
    assert response.json()['detail'] == SuccessMessages.UPDATE_USER  # type: ignore


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
    assert response.json()['detail'] == SuccessMessages.UPDATE_USER  # type: ignore
    assert passwords_match


# @ ============================ Testes de Error ==============================


@pytest.mark.asyncio()
async def test_update_data_without_token_should_return_401_unauthenticated(
    client, faker_user
):
    update_faker_user = {'username': 'user_test'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.NOT_AUTHENTICATED_401  # type: ignore


@pytest.mark.asyncio()
async def test_update_data_with_token_invalid_should_return_401_unauthenticated(
    client, faker_user
):
    update_faker_user = {'username': 'user_test'}

    headers = {'Authorization': 'Bearer token_invalid'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.NOT_VALIDATE_CREDENTIALS_401  # type: ignore


@pytest.mark.asyncio()
async def test_updates_existing_username_should_return_409_conflict_error(
    client, token, faker_user
):
    update_faker_user = {'username': 'usertest'}

    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.USERNAME_ALREADY_EXISTS_409  # type: ignore


@pytest.mark.asyncio()
async def test_updates_existing_email_should_return_409_conflict_error(
    client, token, faker_user
):
    update_faker_user = {'email': 'usertest@example.com'}

    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert 'detail' in response.json()
    assert response.json()['detail'] == ErrorMessages.EMAIL_ALREADY_EXISTS_409  # type: ignore


@pytest.mark.asyncio()
async def test_put_with_user_id_invalid(client, token):
    update_faker_user = {'password': 'myS&cret007'}

    response = client.put(
        '/api/users/999999',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == ErrorMessages.VALUE_ERROR  # type: ignore
    assert response.json()['detail'][0]['msg'] == ErrorMessages.PYDANTIC_OBJECT_ID  # type: ignore


@pytest.mark.asyncio()
async def test_put_non_existent_user(client, token):
    update_faker_user = {'password': 'myS&cret007'}

    response = client.put(
        '/api/users/5eb7cf5a86d9755df3a6c593',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == ErrorMessages.BAD_REQUEST_CHECK_PERMISSION_USER  # type: ignore


@pytest.mark.asyncio()
async def test_required_field_password_put(client, token, faker_user):
    response = client.put(
        f'/api/users/{faker_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY  # 400
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body']


@pytest.mark.asyncio()
async def test_password_validation_lt_8_put(client, token, faker_user):
    update_faker_user = {'password': 'my'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'string_too_short'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_character_uppercase_put(
    client, token, faker_user
):
    update_faker_user = {'password': 'mysecret'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validatest_password_must_contain_least_one_lowercase_letter_put(
    client, token, faker_user
):
    update_faker_user = {
        'password': 'MYS&CRET007',
    }

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_special_character_put(
    client, token, faker_user
):
    update_faker_user = {
        'password': 'mySecret',
    }

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_number_put(client, token, faker_user):
    update_faker_user = {
        'password': 'myS&cret',
    }

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers={'Authorization': f'Bearer {token}'},
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_username_must_only_contain_letters_numbers_underscores_or_periods(
    client, token, faker_user
):
    new_username = {
        'username': 'usert&)st',
    }

    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=new_username, headers=headers
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'username']


@pytest.mark.asyncio()
async def test_updating_username_must_not_contain_excessive_repetition_characters(
    client, token, faker_user
):
    new_username = {'username': 'uuuuuusertest'}

    headers = {'Authorization': f'Bearer {token}'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=new_username, headers=headers
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'username']

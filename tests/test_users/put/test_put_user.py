import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.schema.faker_user import FakerUser
from smartkitchien_api.security.security import verify_password


@pytest.mark.asyncio()
async def test_update_username_returns_200_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'username': 'new_testuser'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_update_email_returns_200_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'email': 'new_testuser@example.com'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_update_password_returns_200_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'newmyS&cret007'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    updated_user = await FakerUser.get(faker_user.id)

    if updated_user:
        passwords_match = verify_password(
            plain_password=update_faker_user['password'],
            hashed_password=updated_user.password,
        )

    assert response.status_code == status.HTTP_200_OK
    assert passwords_match


# @ ============================ Testes de Error ==============================


@pytest.mark.asyncio()
async def test_update_user_returns_401_when_token_missing(
    client: TestClient, faker_user: FakerUser
):
    update_faker_user = {'username': 'test_user'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_update_user_returns_401_when_token_invalid(
    client: TestClient, faker_user: FakerUser
):
    update_faker_user = {'username': 'test_user'}

    headers = {'Authorization': 'Bearer token_invalid'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_update_username_returns_409_when_username_exists(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'username': 'testuser'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_update_email_returns_409_when_email_exists(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'email': 'testuser@example.com'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=update_faker_user, headers=headers
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_update_user_returns_422_when_user_id_invalid(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'myS&cret007'}

    user_id = '999999'

    response = client.put(
        f'/api/users/{user_id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_user_returns_400_when_user_non_existent(
    client: TestClient, headers: dict[str, str]
):
    update_faker_user = {'password': 'myS&cret007'}

    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    response = client.put(
        f'/api/users/{non_existent_user_id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_password_missing(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    response = client.put(
        f'/api/users/{faker_user.id}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_password_too_short(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'my'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_missing_uppercase_character(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'mysecret'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_missing_lowercase_character(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'MYS&CRET007'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_missing_special_character(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'mySecret'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_password_returns_422_when_missing_number(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    update_faker_user = {'password': 'myS&cret'}

    response = client.put(
        f'/api/users/{faker_user.id}',
        json=update_faker_user,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_username_returns_422_when_contains_invalid_characters(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    new_username = {'username': 'usert&)st'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=new_username, headers=headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_username_returns_422_when_contains_excessive_repetition(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    new_username = {'username': 'uuuuutestuser'}

    response = client.put(
        f'/api/users/{faker_user.id}', json=new_username, headers=headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

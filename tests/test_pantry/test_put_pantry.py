import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': '9.99',
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_404_when_pantry_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    item_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_404_when_category_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    category_value = '102'  # user_pantry é uma fixture que tem apenas a categoria 101

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_404_when_item_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_400_when_user_id_lacks_permission(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = '5eb7cf5a86d9755df3a6c593'
    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_422_when_invalid_data(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    category_value = '101'

    item_update = {
        'quantity': 'string',  # quantity é um campo INT
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_401_when_token_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    headers = {'Authorization': 'Bearer invalid_token'}

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_update_item_pantry_returns_401_when_token_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    category_value = '101'

    item_update = {
        'name': 'Pão de Forma',
        'quantity': 2,
        'unit': 'un',
        'price': 9.99,
    }

    response = client.put(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

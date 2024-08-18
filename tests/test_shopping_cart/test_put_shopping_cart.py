import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.shopping_cart import ShoppingCart
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_update_item_shopping_cart_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    category_value = '101'

    item_update = {'name': 'Coca-Cola', 'quantity': 10, 'unit': 'un', 'price': 140}

    response = client.put(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_update_item_shopping_cart_returns_404_when_category_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    # user_shopping_cart é uma fixture que tem apenas a categoria 101
    category_value = '102'

    item_update = {'name': 'Coca-Cola', 'quantity': 10, 'unit': 'un', 'price': 140}

    response = client.put(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_shopping_cart_returns_404_when_item_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    item_update = {'name': 'Coca-Cola', 'quantity': 10, 'unit': 'un', 'price': 140}

    response = client.put(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        json=item_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_item_shopping_returns_400_when_user_id_lacks_permission(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
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

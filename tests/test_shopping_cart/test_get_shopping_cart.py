import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.shopping_cart import ShoppingCart
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_200_when_authenticated(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    response = client.get(f'/api/shopping_cart/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_401_when_unauthenticated(
    client: TestClient,
    faker_user: FakerUser,
):
    response = client.get(f'/api/shopping_cart/{faker_user.id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_401_when_token_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
):
    response = client.get(
        f'/api/shopping_cart/{faker_user.id}',
        headers={'Authorization': 'Bearer token_invalid'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_400_when_user_id_does_not_exist(
    client: TestClient, headers: dict[str, str]
):
    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    response = client.get(f'/api/shopping_cart/{non_existent_user_id}', headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_422_when_user_id_is_invalid(
    client: TestClient, headers: dict[str, str]
):
    invalid_user_id = '9999'

    response = client.get(f'/api/shopping_cart/{invalid_user_id}', headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_get_shopping_cart_returns_404_when_user_has_no_shopping_cart(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    response = client.get(f'/api/shopping_cart/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

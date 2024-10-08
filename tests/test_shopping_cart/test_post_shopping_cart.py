import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchen_api.models.shopping_cart import ShoppingCart
from smartkitchen_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_create_item_returns_201_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio()
async def test_create_item_returns_201_when_in_existing_category(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item2 = {'name': 'Pão de Sal', 'quantity': 4, 'unit': 'un', 'price': 100.46}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item2,
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio()
async def test_create_item_returns_201_when_in_new_category(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    item2 = {'name': 'Pão de Sal', 'quantity': 4, 'unit': 'un', 'price': 100.46}

    category_value = '105'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item2,
    )

    assert response.status_code == status.HTTP_201_CREATED


# @ ===================== TESTES DE ERRO ======================


@pytest.mark.asyncio()
async def test_create_item_returns_401_when_token_is_missing(
    client: TestClient, faker_user: FakerUser
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        json=item,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_create_item_returns_401_when_token_is_invalid(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers={'Authorization': 'Bearer invalid_token'},
        json=item,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_name_is_missing(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_quantity_is_missing(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_unit_is_missing(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_category_is_invalid(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value_invalid = '999'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value_invalid}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_user_id_is_invalid(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    user_id = 'invalid_user_id'

    response = client.post(
        f'/api/shopping_cart/{user_id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_price_is_invalid(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {
        'name': 'Pão de Forma',
        'quantity': 1,
        'unit': 'un',
        'price': 'invalid_price',
    }

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_422_when_price_is_negative(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': -10.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_item_returns_400_when_user_id_lacks_permission(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{non_existent_user_id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_create_item_returns_409_when_item_with_same_name_already_exists(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item = {'name': 'Coca-Cola', 'quantity': 2, 'unit': 'l', 'price': 14}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_409_CONFLICT


@pytest.mark.asyncio()
async def test_create_item_returns_400_when_user_id_is_missing(
    client: TestClient,
    headers: dict[str, str],
):
    item = {'name': 'Pão de Queijo', 'quantity': 3, 'unit': 'un', 'price': 5.99}

    category_value = '101'

    response = client.post(
        f'/api/shopping_cart//category/{category_value}',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_create_item_returns_404_when_category_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    item = {'name': 'Pão de Queijo', 'quantity': 3, 'unit': 'un', 'price': 5.99}

    response = client.post(
        f'/api/shopping_cart/{faker_user.id}/category/',
        headers=headers,
        json=item,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

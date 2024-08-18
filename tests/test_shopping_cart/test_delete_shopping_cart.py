import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.shopping_cart import ShoppingCart
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_delete_item_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    category_value = '101'

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_delete_item_returns_200_when_ensures_data_integrity_after_deletion(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}
    item2 = {'name': 'Pão de Sal', 'quantity': 10, 'unit': 'un', 'price': 1.99}

    category_values = ['101', '102', '103']

    for category_value in category_values:
        client.post(
            f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=item,
        )

        client.post(
            f'/api/shopping_cart/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=item2,
        )

    initial_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == faker_user.id
    ).first_or_none()

    assert initial_shopping_cart is not None

    # Seleciona a primeira categoria e o primeiro item dessa categoria para deletar
    category_value = initial_shopping_cart.shopping_cart[0].category_value.value
    # O .value é porque ele é um (Enum)

    item_id_to_delete = initial_shopping_cart.shopping_cart[0].items[0].id

    # Guarda a quantidade de categorias e itens antes da exclusão
    initial_category_count = len(initial_shopping_cart.shopping_cart)
    initial_item_count_in_category = len(initial_shopping_cart.shopping_cart[0].items)

    # Realiza a exclusão do item
    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id_to_delete}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK

    # Verifica se o item foi removido, mas a estrutura do Pantry foi preservada
    updated_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == faker_user.id
    ).first_or_none()

    assert updated_shopping_cart is not None

    # Verifica que a quantidade de categorias permaneceu a mesma
    assert len(updated_shopping_cart.shopping_cart) == initial_category_count

    # Verifica que a quantidade de itens na categoria foi decrementada
    assert (
        len(updated_shopping_cart.shopping_cart[0].items)
        == initial_item_count_in_category - 1
    )

    # Verifica que os outros itens e categorias permanecem inalterados
    remaining_items_ids = [
        item.id for item in updated_shopping_cart.shopping_cart[0].items
    ]
    assert item_id_to_delete not in remaining_items_ids


# @ =================== TESTES DE ERROR ====================


@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_item_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = 'invalid_id'

    category_value = '101'

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_item_id_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    category_value = '101'
    valid_but_nonexistent_item_id = '64b4e13c8c33524b7b47d0f3'

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{valid_but_nonexistent_item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_item_returns_401_when_token_is_missing(
    client: TestClient, faker_user: FakerUser, user_shopping_cart: ShoppingCart
):
    category_value = '101'

    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_item_returns_401_when_token_is_invalid(
    client: TestClient, faker_user: FakerUser, user_shopping_cart: ShoppingCart
):
    category_value = '101'

    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{category_value}',
        headers={'Authorization': 'Bearer token_invalido'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_user_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    category_value = '101'

    invalid_user_id = 'invalid_user_id'

    response = client.delete(
        f'/api/shopping_cart/{invalid_user_id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_user_id_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    category_value = '101'

    user_id = '5eb7cf5a86d9755df3a6c593'

    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    response = client.delete(
        f'/api/shopping_cart/{user_id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_user_id_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    category_value = '101'

    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    response = client.delete(
        f'/api/shopping_cart/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_category_value_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    invalid_category_value = 'invalid_category'

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}/category/{invalid_category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_category_value_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_shopping_cart: ShoppingCart,
):
    item_id = user_shopping_cart.shopping_cart[0].items[0].id

    response = client.delete(
        f'/api/shopping_cart/{faker_user.id}/item/{item_id}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

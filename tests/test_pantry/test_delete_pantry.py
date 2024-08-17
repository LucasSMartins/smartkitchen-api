import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_delete_item_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    category_value = '101'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    pantry_empty = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_200_OK
    assert pantry_empty is None


@pytest.mark.asyncio()
async def test_delete_item_returns_200_when_ensures_data_integrity_after_deletion(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}
    item2 = {'name': 'Pão de Sal', 'quantity': 10, 'unit': 'un', 'price': 1.99}

    category_values = ['101', '102', '103']

    for category_value in category_values:
        client.post(
            f'/api/pantry/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=item,
        )

        client.post(
            f'/api/pantry/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=item2,
        )

    initial_pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert initial_pantry is not None

    # Seleciona a primeira categoria e o primeiro item dessa categoria para deletar
    category_value = initial_pantry.pantry[0].category_value.value
    # O .value é porque ele é um (Enum)

    item_id_to_delete = initial_pantry.pantry[0].items[0].id

    # Guarda a quantidade de categorias e itens antes da exclusão
    initial_category_count = len(initial_pantry.pantry)
    initial_item_count_in_category = len(initial_pantry.pantry[0].items)

    # Realiza a exclusão do item
    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{item_id_to_delete}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK

    # Verifica se o item foi removido, mas a estrutura do Pantry foi preservada
    updated_pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert updated_pantry is not None

    # Verifica que a quantidade de categorias permaneceu a mesma
    assert len(updated_pantry.pantry) == initial_category_count

    # Verifica que a quantidade de itens na categoria foi decrementada
    assert len(updated_pantry.pantry[0].items) == initial_item_count_in_category - 1

    # Verifica que os outros itens e categorias permanecem inalterados
    remaining_items_ids = [item.id for item in updated_pantry.pantry[0].items]
    assert item_id_to_delete not in remaining_items_ids


# @ =================== TESTES DE ERROR ====================
@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_item_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    category_value = '101'
    invalid_item_id = 'invalid_id'

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{invalid_item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_item_id_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    category_value = '101'
    valid_but_nonexistent_item_id = '64b4e13c8c33524b7b47d0f3'

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{valid_but_nonexistent_item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_item_returns_401_when_token_is_missing(
    client: TestClient, faker_user: FakerUser, user_pantry: Pantry
):
    category_value = '101'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_item_returns_401_when_token_is_invalid(
    client: TestClient, faker_user: FakerUser, user_pantry: Pantry
):
    category_value = '101'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{category_value}',
        headers={'Authorization': 'Bearer token_invalido'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_user_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    invalid_user_id = 'invalid_user_id'
    category_value = '101'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{invalid_user_id}/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_user_id_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    category_value = '101'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/item/{item_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_item_returns_422_when_category_value_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    invalid_category_value = 'invalid_category'
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{faker_user.id}/item/{item_id}/category/{invalid_category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_item_returns_404_when_category_value_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_pantry: Pantry,
):
    item_id = user_pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{faker_user.id}/category//item/{item_id}', headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

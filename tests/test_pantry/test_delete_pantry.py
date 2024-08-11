import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.pantry import Pantry


@pytest.mark.asyncio()
async def test_delete_item(client, token, faker_user):
    # Criando o item a ser deletado.
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id

    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    item_id = pantry.pantry[0].items[0].id

    response = client.delete(
        f'/api/pantry/{user_id}/category/{category_value}/item/{item_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Se houver apenas um item na lista com apenas uma categoria e ele
    # for deletado, o Pantry tbm é deletado.
    pantry_empty = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == SuccessMessages.ITEM_DELETED  # type: ignore
    assert pantry_empty is None


# @ =================== TESTES DE ERROR ====================
@pytest.mark.asyncio()
async def test_delete_item_pantry_with_invalid_item_id(client, token, faker_user):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id
    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    invalid_item_id = 'invalid_id'

    # Tentando deletar um item com ID inválido
    response = client.delete(
        f'/api/pantry/{user_id}/category/{category_value}/item/{invalid_item_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['path', 'item_id']  # type: ignore


@pytest.mark.asyncio()
async def test_delete_item_pantry_with_valid_item_id_but_not_found(
    client, token, faker_user
):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id
    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    valid_but_nonexistent_item_id = '64b4e13c8c33524b7b47d0f3'

    # Tentando deletar um item com um ID válido, mas que não existe
    response = client.delete(
        f'/api/pantry/{user_id}/category/{category_value}/item/{valid_but_nonexistent_item_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == ErrorMessages.ITEM_NOT_FOUND  # type: ignore


# Teste para deletar item com token ausente
@pytest.mark.asyncio()
async def test_delete_item_pantry_without_token(client, faker_user, token):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id
    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()
    item_id = pantry.pantry[0].items[0].id

    # Tentando deletar item sem token
    response = client.delete(
        f'/api/pantry/{user_id}/category/{category_value}/item/{item_id}',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_AUTHENTICATED_401}


# Teste para deletar item com token inválido
@pytest.mark.asyncio()
async def test_delete_item_pantry_with_invalid_token(client, faker_user, token):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id
    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        json=item_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()
    item_id = pantry.pantry[0].items[0].id

    # Tentando deletar item com token inválido
    response = client.delete(
        f'/api/pantry/{user_id}/category/{category_value}/item/{item_id}',
        headers={'Authorization': 'Bearer token_invalido'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_VALIDATE_CREDENTIALS_401}


@pytest.mark.asyncio()
async def test_delete_item_pantry_with_invalid_user_id(client, token):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    invalid_user_id = 'invalid_user_id'
    category_value = '101'

    client.post(
        f'/api/pantry/{invalid_user_id}/category/{category_value}',
        json=item_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    pantry = await Pantry.find(Pantry.user_id == invalid_user_id).first_or_none()
    item_id = pantry.pantry[0].items[0].id if pantry else 'invalid_item_id'

    # Tentando deletar item com user_id inválido
    response = client.delete(
        f'/api/pantry/{invalid_user_id}/category/{category_value}/item/{item_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['path', 'user_id']  # type: ignore


# @pytest.mark.asyncio()
# async def test_delete_item_pantry_with_user_id_user_that_does_not_exist(
#     client, token, faker_user
# ):
#     pass


@pytest.mark.asyncio()
async def test_delete_item_pantry_without_user_id(client, token, faker_user):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'
    user_id = faker_user.id

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        json=item_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    # Tentando deletar item sem user_id
    response = client.delete(
        f'/api/pantry/category/{category_value}/item/invalid_item_id',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


# Teste para deletar item com category_value inválido
@pytest.mark.asyncio()
async def test_delete_item_pantry_with_invalid_category_value(
    client, token, faker_user
):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id
    invalid_category_value = 'invalid_category'

    client.post(
        f'/api/pantry/{user_id}/category/{invalid_category_value}',
        json=item_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()
    item_id = pantry.pantry[0].items[0].id if pantry else 'invalid_item_id'

    # Tentando deletar item com category_value inválido
    response = client.delete(
        f'/api/pantry/{user_id}/category/{invalid_category_value}/item/{item_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['path', 'item_id']  # type: ignore


# Teste para deletar item com category_value ausente
@pytest.mark.asyncio()
async def test_delete_item_pantry_without_category_value(client, token, faker_user):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id

    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    user_id = faker_user.id

    # Tentando deletar item sem category_value
    response = client.delete(
        f'/api/pantry/{user_id}/category//item/invalid_item_id',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

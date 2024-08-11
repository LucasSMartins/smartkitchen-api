import pytest
from fastapi import status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.pantry import Pantry


@pytest.mark.asyncio()
async def test_create_item_pantry(client, token, faker_user):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.ITEM_ADDED}
    assert pantry is not None
    assert len(pantry.pantry) > 0
    assert len(pantry.pantry[0].items) > 0


@pytest.mark.asyncio()
async def test_create_item_pantry_in_an_existing_category(client, token, faker_user):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}
    item2 = {'name': 'Pão de Sal', 'quantity': 4, 'unit': 'un', 'price': 100.46}

    user_id = faker_user.id

    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item2,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.ITEM_ADDED}
    assert pantry is not None
    assert len(pantry.pantry) > 0
    assert len(pantry.pantry[0].items) > 1


@pytest.mark.asyncio()
async def test_create_item_pantry_in_an_new_category(client, token, faker_user):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}
    item2 = {'name': 'Pão de Sal', 'quantity': 4, 'unit': 'un', 'price': 100.46}
    item3 = {'name': 'Pão de Doce', 'quantity': 2, 'unit': 'un', 'price': 3}

    user_id = faker_user.id

    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item2,
    )

    new_category_value = '105'

    response = client.post(
        f'/api/pantry/{user_id}/category/{new_category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item3,
    )

    pantry = await Pantry.find(Pantry.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.ITEM_ADDED}
    assert pantry is not None
    assert len(pantry.pantry) > 1  # list of categories
    assert len(pantry.pantry[0].items) > 1  # category 101
    assert len(pantry.pantry[1].items) > 0  # new category 105


# @ ==================== TESTES DE ERROR ======================


@pytest.mark.asyncio()
async def test_create_item_pantry_without_token(client, faker_user):
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = str(faker_user.id)

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        json=item,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_AUTHENTICATED_401}


@pytest.mark.asyncio()
async def test_create_item_pantry_with_invalid_token(client, faker_user):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = str(faker_user.id)

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': 'Bearer token_invalido'},
        json=item_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_VALIDATE_CREDENTIALS_401}


@pytest.mark.asyncio()
async def test_create_item_pantry_without_name(client, token, faker_user):
    item_data = {
        'quantity': 1,
        'unit': 'un',
        'price': 10.99,
    }

    user_id = str(faker_user.id)

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'name']


@pytest.mark.asyncio()
async def test_create_item_pantry_without_quantity(client, token, faker_user):
    item_data = {
        'name': 'Pão de Forma',
        'unit': 'un',
        'price': 10.99,
    }

    user_id = str(faker_user.id)

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'quantity']


@pytest.mark.asyncio()
async def test_create_item_pantry_with_invalid_category(client, token, faker_user):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = str(faker_user.id)

    category_value_invalid = '999'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value_invalid}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'enum'
    assert msg['loc'] == ['path', 'category_value']


@pytest.mark.asyncio()
async def test_create_item_pantry_with_invalid_user_id(client, token):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    category_value = '101'

    response = client.post(
        f'/api/pantry/999/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['path', 'user_id']  # type: ignore


@pytest.mark.asyncio()
async def test_create_item_pantry_with_invalid_price(client, token, faker_user):
    item_data = {
        'name': 'Pão de Forma',
        'quantity': 1,
        'unit': 'un',
        'price': 'invalid_price',
    }

    user_id = str(faker_user.id)

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'decimal_parsing'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['body', 'price']  # type: ignore


@pytest.mark.asyncio()
async def test_create_item_pantry_with_user_id_without_permission(
    client, token, faker_user
):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == ErrorMessages.BAD_REQUEST_CHECK_PERMISSION_USER  # type: ignore


@pytest.mark.asyncio()
async def test_checks_if_an_item_with_the_same_name_already_exists(
    client, faker_user, token
):
    item_data = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    user_id = faker_user.id

    category_value = '101'

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    response = client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item_data,
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json()['detail'] == ErrorMessages.ITEM_ALREADY_EXISTS  # type: ignore

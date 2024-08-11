import pytest
from fastapi import HTTPException, status

from smartkitchien_api.api.routes.cookbook.post import add_item_to_list
from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.cookbook import Cookbook
from smartkitchien_api.schema.enums.category_value import CategoryValue
from smartkitchien_api.schema.recipe import Recipe


@pytest.mark.asyncio()
async def test_create_recipe(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.RECIPE_CREATED}
    assert cookbook is not None
    assert len(cookbook.cookbook)  # Verificar se a categoria foi criada
    assert len(
        cookbook.cookbook[0].items
    )  # Verificar se a receita foi adicionada à lista da categoria


@pytest.mark.asyncio()
async def test_create_recipe_in_an_existing_category(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    recipe_data2 = {
        'name': 'Recipe Example 2',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 2,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita
    client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data2,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {'detail': SuccessMessages.RECIPE_CREATED}
    assert cookbook is not None
    assert len(cookbook.cookbook)  # Verificar se a categoria foi criada
    assert len(
        cookbook.cookbook[0].items
    )  # Verificar se a receita foi adicionada à lista da categoria


# @ ==================== TESTES DE ERROR ======================
@pytest.mark.asyncio()
async def test_create_recipe_without_token(client, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem token
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_AUTHENTICATED_401}


@pytest.mark.asyncio()
async def test_create_recipe_with_invalid_token(client, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita com token inválido
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': 'Bearer token_invalido'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': ErrorMessages.NOT_VALIDATE_CREDENTIALS_401}


@pytest.mark.asyncio()
async def test_create_recipe_without_name(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem nome
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'name']


@pytest.mark.asyncio()
async def test_create_recipe_without_ingredients(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem ingredientes
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'ingredients']


@pytest.mark.asyncio()
async def test_create_recipe_with_invalid_category(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '99:99',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    category_value_invalid = '999'

    # Fazer a requisição POST para criar uma receita com categoria inválida
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value_invalid}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'enum'
    assert msg['loc'] == ['path', 'category_value']


@pytest.mark.asyncio()
async def test_create_recipe_with_invalid_user_id(client, token):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita com ID de usuário inválido
    response = client.post(
        f'/api/cookbook/999/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'value_error'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['path', 'user_id']  # type: ignore


@pytest.mark.asyncio()
async def test_create_recipe_with_invalid_preparation_time(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '99:aa',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita com tempo de preparo inválido
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'string_pattern_mismatch'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['body', 'preparation_time']  # type: ignore


@pytest.mark.asyncio()
async def test_create_recipe_with_invalid_portion(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': -1,
    }

    # Obter o ID do usuário
    user_id = str(faker_user.id)

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita com porção inválida
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['type'] == 'greater_than'  # type: ignore
    assert response.json()['detail'][0]['loc'] == ['body', 'portion']  # type: ignore


@pytest.mark.asyncio()
async def test_create_recipe_with_user_id_without_permission(client, token, faker_user):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 1,
    }

    # Obter o ID do usuário
    user_id = '5eb7cf5a86d9755df3a6c593'

    # Definir o valor da categoria
    category_value = '101'

    # Fazer a requisição POST para criar uma receita com porção inválida
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == ErrorMessages.BAD_REQUEST_CHECK_PERMISSION_USER  # type: ignore

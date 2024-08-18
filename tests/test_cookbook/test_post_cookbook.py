import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.models.cookbook import Cookbook
from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_create_recipe_return_200_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict[str, str]
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert cookbook is not None
    assert len(cookbook.cookbook) > 0  # Verificar se a categoria foi criada
    assert (
        len(cookbook.cookbook[0].items) > 0
    )  # Verificar se a receita foi adicionada à lista da categoria


@pytest.mark.asyncio()
async def test_create_recipe_returns_201_when_adding_an_item_to_an_existing_category(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
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

    category_value = '101'

    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data2,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert cookbook is not None
    assert len(cookbook.cookbook)  # Verificar se a categoria foi criada
    assert len(
        cookbook.cookbook[0].items
    )  # Verificar se a receita foi adicionada à lista da categoria


@pytest.mark.asyncio()
async def test_create_recipe_returns_201_when_adding_item_to_new_category(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
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

    new_category_value = '105'

    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{new_category_value}',
        headers=headers,
        json=recipe_data2,
    )

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    assert response.status_code == status.HTTP_201_CREATED
    assert cookbook is not None
    assert len(cookbook.cookbook) > 1  # list of categories
    assert len(cookbook.cookbook[0].items) > 0  # category 101
    assert len(cookbook.cookbook[1].items) > 0  # new category 105


# @ ==================== TESTES DE ERROR ======================
@pytest.mark.asyncio()
async def test_create_recipe_returns_401_when_token_is_missing(
    client: TestClient,
    faker_user: FakerUser,
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem token
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_create_recipe_returns_401_when_token_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita com token inválido
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers={'Authorization': 'Bearer token_invalido'},
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_create_recipe_returns_404_when_the_name_field_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem nome
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_404_when__the_ingredients_field_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    # Definir os dados da receita conforme solicitado
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'method_preparation': 'String',
        'portion': 4,
    }

    category_value = '101'

    # Fazer a requisição POST para criar uma receita sem ingredientes
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_category_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
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

    category_value_invalid = '999'

    # Fazer a requisição POST para criar uma receita com categoria inválida
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value_invalid}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_user_id_is_invalid(
    client: TestClient,
    headers: dict[str, str],
):
    user_id = '999'

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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita com ID de usuário inválido
    response = client.post(
        f'/api/cookbook/{user_id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_preparation_time_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita com tempo de preparo inválido
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_portion_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
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

    category_value = '101'

    # Fazer a requisição POST para criar uma receita com porção inválida
    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_400_when_user_id_without_permission(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
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

    non_existent_user_id = '5eb7cf5a86d9755df3a6c593'

    category_value = '101'

    # Fazer a requisição POST para criar uma receita com porção inválida
    response = client.post(
        f'/api/cookbook/{non_existent_user_id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_ingredients_are_empty(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [],
        'method_preparation': 'String',
        'portion': 4,
    }

    category_value = '101'

    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_method_preparation_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    recipe_data = {
        'name': 'Recipe Example',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'portion': 4,
    }

    category_value = '101'

    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_create_recipe_returns_422_when_json_format_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    recipe_data = 'invalid_json_format'

    category_value = '101'

    response = client.post(
        f'/api/cookbook/{faker_user.id}/category/{category_value}',
        headers=headers,
        json=recipe_data,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

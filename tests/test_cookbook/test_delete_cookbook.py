import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchen_api.models.cookbook import Cookbook
from smartkitchen_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_delete_recipe_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '101'
    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_delete_recipe_returns_200_when_ensures_data_integrity_after_deletion(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_values = ['102', '103']
    """
        101 - len 1
        102 - len 2
        103 - len 2

        cookbook - len 3 (101, 102, 103)
    """

    recipe2 = {
        'name': 'Recipe Example2',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    recipe3 = {
        'name': 'Recipe Example3',
        'preparation_time': '01:30',
        'ingredients': [
            {'name': 'string', 'quantity': 'string'},
            {'name': 'string', 'quantity': 'string'},
        ],
        'method_preparation': 'String',
        'portion': 4,
    }

    for category_value in category_values:
        client.post(
            f'/api/cookbook/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=recipe2,
        )

        client.post(
            f'/api/cookbook/{faker_user.id}/category/{category_value}',
            headers=headers,
            json=recipe3,
        )

    initial_cookbook = await Cookbook.find(
        Cookbook.user_id == faker_user.id
    ).first_or_none()

    assert initial_cookbook is not None

    # Seleciona a primeira categoria e a primeira receita dessa categoria para deletar
    category_value = initial_cookbook.cookbook[0].category_value.value
    # O .value é porque ele é um (Enum) - 101

    recipe_id_to_delete = initial_cookbook.cookbook[0].items[0].id

    # Guarda a quantidade de categorias e itens antes da exclusão
    # len 3 , por ter 3 categorias.
    initial_category_count = len(initial_cookbook.cookbook)

    # Realiza a exclusão da receita
    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id_to_delete}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK

    # Verifica se a receita foi removida, mas a estrutura foi preservada
    """
        101 - len 0
        102 - len 2
        103 - len 2

        cookbook - len 2 (102, 103)
    """
    updated_cookbook = await Cookbook.find(
        Cookbook.user_id == faker_user.id
    ).first_or_none()

    assert updated_cookbook is not None

    # Verifica que a quantidade de categorias foi decrementada
    assert len(updated_cookbook.cookbook) != initial_category_count

    expected_length_of_cookbook_list = 2

    assert len(updated_cookbook.cookbook) == expected_length_of_cookbook_list


# @ =================== TESTES DE ERROR ====================


@pytest.mark.asyncio()
async def test_delete_recipe_returns_401_when_token_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    user_cookbook: Cookbook,
):
    category_value = '101'

    recipe_id = user_cookbook.cookbook[0].items[0].id

    headers = {'Authorization': 'Bearer invalid_token'}

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_recipe_returns_401_when_token_is_missing(
    client: TestClient, faker_user: FakerUser, user_cookbook: Cookbook
):
    category_value = '101'

    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_delete_recipe_returns_404_when_user_id_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '101'

    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook//recipe/{recipe_id}/category/{category_value}',
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_recipe_returns_404_when_category_value_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_recipe_returns_404_when_recipe_id_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '101'

    recipe_id = '5eb7cf5a86d9755df3a6c593'

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_delete_recipe_returns_422_when_recipe_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '101'

    recipe_id = 'invalid_id'

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_recipe_returns_422_when_user_id_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '101'

    user_id = 'invalid_id'

    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook/{user_id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_delete_recipe_returns_422_when_category_value_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    category_value = '9999'

    recipe_id = user_cookbook.cookbook[0].items[0].id

    response = client.delete(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

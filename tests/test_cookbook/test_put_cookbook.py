import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchen_api.models.cookbook import Cookbook
from smartkitchen_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_200_when_successful(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_200_OK

    cookbook = await Cookbook.find(Cookbook.user_id == faker_user.id).first_or_none()

    if cookbook:
        assert cookbook.cookbook[0].items[0].name == 'new_string'
        assert cookbook.cookbook[0].items[0].preparation_time == '40:00'
        assert cookbook.cookbook[0].items[0].method_preparation == 'new_string'
        assert cookbook.cookbook[0].items[0].portion == 1
        assert len(cookbook.cookbook[0].items[0].ingredients) != len(
            user_cookbook.cookbook[0].items[0].ingredients  # type: ignore
        )


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_404_when_cookbook_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
):
    recipe_id = '60c8c6b8a9b8b4e8b4f8b4e8'

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_404_when_category_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '102'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_404_when_recipe_not_found(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = '60c8c6b8a9b8b4e8b4f8b4e8'

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_400_when_user_id_lacks_permission(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    user_id = '60c8c6b8a9b8b4e8b4f8b4e8'

    response = client.put(
        f'/api/cookbook/{user_id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_422_when_invalid_data(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '101'

    recipe_update = {
        'portion': 'string',  # Deve ser um inteiro
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_401_when_token_is_invalid(
    client: TestClient,
    faker_user: FakerUser,
    headers: dict[str, str],
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    headers['Authorization'] = 'Bearer invalid_token'

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
        headers=headers,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio()
async def test_update_recipe_cookbook_returns_401_when_token_is_missing(
    client: TestClient,
    faker_user: FakerUser,
    user_cookbook: Cookbook,
):
    recipe_id = user_cookbook.cookbook[0].items[0].id

    category_value = '101'

    recipe_update = {
        'name': 'new_string',
        'preparation_time': '40:00',
        'ingredients': [
            {'name': 'new_string', 'quantity': 'new_string'},
        ],
        'method_preparation': 'new_string',
        'portion': 1,
    }

    response = client.put(
        f'/api/cookbook/{faker_user.id}/recipe/{recipe_id}/category/{category_value}',
        json=recipe_update,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

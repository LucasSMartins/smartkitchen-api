import pytest
from fastapi import status

from smartkitchien_api.models.pantry import PantryPublic


@pytest.mark.asyncio()
async def test_get_user_pantry(client, faker_user, token):
    user_id = faker_user.id
    headers = {'Authorization': f'Bearer {token}'}
    category_value = '101'
    item = {'name': 'Pão de Forma', 'quantity': 1, 'unit': 'un', 'price': 10.99}

    client.post(
        f'/api/pantry/{user_id}/category/{category_value}',
        headers={'Authorization': f'Bearer {token}'},
        json=item,
    )

    response = client.get(f'/api/pantry/{user_id}', headers=headers)

    pantry = response.json()['detail']

    pantry_public = PantryPublic(**pantry)

    assert response.status_code == status.HTTP_200_OK
    assert 'detail' in response.json()
    assert isinstance(pantry, dict)
    assert isinstance(pantry['pantry'], list)
    assert len(pantry['pantry']) >= 1
    assert isinstance(pantry_public, PantryPublic)

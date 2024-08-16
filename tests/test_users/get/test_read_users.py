import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.schema.faker_user import FakerUser


@pytest.mark.asyncio()
async def test_read_users_returns_200_with_list_of_users_when_successful(
    client: TestClient, faker_user: FakerUser, another_faker_user: FakerUser
):
    # Teste para leitura de todos os usuários quando existem usuários cadastrados
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_read_users_returns_404_when_no_users_exist(client):
    # Teste para leitura de todos os usuários quando não existem usuários cadastrados
    response = client.get('/api/users')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio()
async def test_read_user_me_returns_200_with_current_user_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict
):
    # Teste para leitura do usuário atual (me)
    response = client.get('/api/users/me', headers=headers)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio()
async def test_read_user_by_id_returns_200_with_user_data_when_successful(
    client: TestClient, faker_user: FakerUser, headers: dict
):
    # Teste para leitura das informações de um usuário específico pelo ID

    response = client.get(f'/api/users/{faker_user.id}', headers=headers)

    assert response.status_code == status.HTTP_200_OK

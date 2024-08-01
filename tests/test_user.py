# import pytest
# from beanie import init_beanie
# from fastapi import status
# from fastapi.testclient import TestClient
# from mongomock_motor import AsyncMongoMockClient  # type: ignore

# from smartkitchien_api.main import app
# from smartkitchien_api.models.user import User


# @pytest.fixture(autouse=True)
# async def my_fixture():
#     client = AsyncMongoMockClient()
#     await init_beanie(document_models=[User], database=client.get_database(name='db'))
#     return client


# @pytest.mark.asyncio()
# async def test_read_users_empty(my_fixture):
#     with TestClient(app) as client:
#         response = client.get('/')
#     assert response.status_code == status.HTTP_200_OK
#     # assert response.status_code == status.HTTP_404_NOT_FOUND
#     # assert response.json() == {'detail': 'Nenhum usuário foi encontrado'}


# @pytest.mark.asyncio()
# async def test_read_users(my_fixture):
#     user = User(**{
#         'username': 'usertest',
#         'email': 'usertest@example.com',
#         'password': 'myS&cret007',
#     })

#     await user.insert()

#     with TestClient(app) as client:
#         response = client.get('/')
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()) == 1
#     assert response.json()[0]['username'] == 'usertest'
#     assert response.json()[0]['email'] == 'usertest@example.com'

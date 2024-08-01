# import pytest
# from beanie import init_beanie
# from mongomock_motor import AsyncMongoMockClient  # type: ignore

# from smartkitchien_api.models.user import User


# @pytest.fixture(autouse=True)
# async def my_fixture():
#     client = AsyncMongoMockClient()
#     # Inicializa o Beanie com o cliente MongoMock
#     await init_beanie(document_models=[User], database=client.get_database(name='db'))

#     return client

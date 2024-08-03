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


# ++++++++++++++++++++++++++++++++++


# @pytest_asyncio.fixture(autouse=True)
# async def init_mongo():
#     client = AsyncMongoMockClient()
#     await init_beanie(document_models=[Meh], database=client.get_database(name='db'))


# @pytest.mark.asyncio()
# async def test_beanie_decimal128():
#     json_data = '{"price": 1.5}'
#     doc = TypeAdapter(Meh).validate_json(json_data)
#     assert doc.price == Decimal('1.5')

#     await doc.save()
#     assert doc.price == Decimal('1.5')

#     assert Meh.find_one().price == Decimal('1.5')

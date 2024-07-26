# from decimal import ROUND_DOWN, Decimal, getcontext
# from typing import Annotated

# from bson import ObjectId
# from fastapi import (
#     APIRouter,
#     Body,
#     Depends,
#     HTTPException,
#     Path,
#     Query,
#     status,
# )

# from smartkitchen_api.api.schema.default_answer import DefaultAnswer, StatusMsg
# from smartkitchen_api.api.schema.shopping_cart import (
#     CategoryValue,
#     ItemsIn,
#     ItemsOut,
# )
# from smartkitchen_api.middleware.validate_object_id import validate_object_id
# from smartkitchen_api.models.connection_options.mongo_db_config import (
#     mongo_db_infos,
# )
# from smartkitchen_api.models.open_connection import open_connection
# from smartkitchen_api.services.pantry_service import get_default_pantry_model

# router = APIRouter()

# collection_repository = open_connection(
#     mongo_db_infos['COLLECTIONS']['collection_shopping_cart']  # type: ignore
# )


# @router.get(
#     '/{user_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def read_shopping_cart(user_id: str = Depends(validate_object_id)):
#     """
#     Route that returns the shopping cart of all users.
#     """
#     filter_document = {'user_id': ObjectId(user_id)}
#     request_attribute = {'_id': 0}

#     data = await collection_repository.find_document_one(
#         filter_document, request_attribute
#     )

#     if not data:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='shopping cart not found'
#             ).model_dump(),
#         )
#     else:
#         data[0]['user_id'] = str(data[0]['user_id'])

#     return DefaultAnswer(status=StatusMsg.SUCCESS, msg='User found', data=data)


# @router.post(
#     '/{user_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def create_cart_item(
#     category_value: Annotated[
#         CategoryValue,
#         Path(
#             description='List of food category values, '
#             'is a 3-digit integer value',
#         ),
#     ],
#     data_items: Annotated[
#         ItemsIn,
#         Body(
#             description='Item data that will be inserted '
#             'into the shopping cart'
#         ),
#     ],
#     user_id: str = Depends(validate_object_id),
# ):
#     """
#     **List of food category values**\n
#     Candy = 101,\n
#     Frozen = 102,\n
#     Drinks = 103,\n
#     Laundry = 104,\n
#     Meat and Fish = 105,\n
#     Dairy and Eggs = 106,\n
#     Grocery Products = 107,\n
#     Personal hygiene = 108,\n
#     Grains and Cereals = 109,\n
#     Cleaning materials = 110,\n
#     Fruits and vegetables = 111,\n
#     Condiments and Sauces = 112,\n
#     Pasta and Wheat Products = 113,\n
#     Breads and Bakery Products = 114,\n
#     Canned goods and preserves = 115,\n
#     """

#     result_find = await collection_repository.find_document_one(
#         filter_document={'user_id': ObjectId(user_id)},
#         request_attribute={'_id': 0, 'password': 0},
#     )

#     if not result_find:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='shopping cart not found'
#             ).model_dump(),
#         )

#     # TODO: Esse ItemOut é similar ao do /pantry,
#     #  e eu ainda coloquei o mesmo nome aqui
#     #  será que é PS.  # noqa: E501

#     data_items_dict = data_items.model_dump()

#     # Convertendo o valor de price para str, pois o DB não
#     # aceita o tipo decimal.
#     if isinstance(data_items.price, Decimal):
#         # Configurar a precisão das operações decimais para 10 dígitos
#         getcontext().prec = 10

#         data_items_dict['price'] = str(
#             data_items_dict['price'].quantize(Decimal('0.01'), ROUND_DOWN)
#         )

#     item_id = ObjectId()

#     data = ItemsOut(item_id=item_id, **data_items_dict)

#     request_attribute = {
#         '$addToSet': {'shoppingCart.$.items': data.model_dump()}
#     }

#     filter_document = {
#         'user_id': ObjectId(user_id),
#         'shoppingCart.category_value': category_value,
#     }

#     update_result = await collection_repository.update_document(
#         filter_document, request_attribute
#     )

#     # TODO: Faz sentido criar uma func. que busque pela user e outra
#     #  pela categoria para ter uma resposta mais correta.?
#     if update_result.matched_count == 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='User or category not found'
#             ).model_dump(),
#         )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS, msg='Item created successfully'
#     )


# # Obter todos os itens de uma categoria específica:
# @router.get(
#     '/category/{user_id}',
#     response_model=DefaultAnswer,
#     status_code=status.HTTP_200_OK,
# )
# async def all_items_specific_category(
#     category_value: Annotated[
#         CategoryValue,
#         Query(
#             description='List of food category values, '
#             'is a 3-digit integer value'
#         ),
#     ],
#     user_id: str = Depends(validate_object_id),
# ):
#     filter_document = {
#         'user_id': ObjectId(user_id),
#         'shoppingCart.category_value': category_value,
#     }

#     request_attribute = {'_id': 0, 'shoppingCart.$': 1}

#     # Verifica se o usuário existe
#     existing_user = await collection_repository.find_document_one({
#         'user_id': ObjectId(user_id)
#     })

#     if not existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='User not found'
#             ).model_dump(),
#         )

#     result_find = await collection_repository.find_document_one(
#         filter_document, request_attribute
#     )

#     if not result_find:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='Category not found'
#             ).model_dump(),
#         )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS,
#         msg='shopping cart Items Found',
#         data=result_find,
#     )


# # Atualizar um item específico de uma categoria
# @router.delete(
#     '/{item_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def delete_item(
#     item_id: Annotated[
#         str, Path(description='Unique ID of the shopping cart item')
#     ],
#     category_value: Annotated[
#         CategoryValue,
#         Query(
#             description='List of food category values, '
#             'is a 3-digit integer value'
#         ),
#     ],
#     user_id: str = Depends(validate_object_id),
# ):
#     filter_document = {
#         'user_id': ObjectId(user_id),
#         'shoppingCart.category_value': category_value,
#         'shoppingCart.items.item_id': item_id,
#     }

#     request_attribute = {
#         '$pull': {'shoppingCart.$[element].items': {'item_id': item_id}}
#     }

#     # array_filters = [{"category.category_value": category_value}]
#     array_filters = [{'element.category_value': category_value}]

#     # Atualiza o documento removendo o item com o item_id especificado
#     update_result = await collection_repository.update_document(
#         filter_document=filter_document,  # Localiza o item
#         request_attribute=request_attribute,  # Aplica a ação [remover o item]
#         array_filters=array_filters,  # Condição
#         # O operador posicional $[<identifier>] irá atuar como um espaço
#         # reservado para todos os elementos do campo selecionado que
#         # correspondem às condições que foram especificadas no arrayFiltros.
#     )

#     if update_result.modified_count == 0:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='No items were found'
#             ).model_dump(),
#         )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS, msg='Item deleted successfully'
#     )


# @router.put(
#     '/{user_id}/category_value/{category_value}',
#     response_model=DefaultAnswer,
#     status_code=status.HTTP_200_OK,
# )
# async def updates_shopping_cart_item(
#     item_id: Annotated[
#         str, Path(description='Unique ID of the shopping cart item')
#     ],
#     category_value: Annotated[
#         CategoryValue,
#         Path(
#             description='List of food category values, '
#             'is a 3-digit integer value'
#         ),
#     ],
#     data_items_update: Annotated[
#         ItemsIn,
#         Body(
#             description='Item data that will be inserted '
#             'into the shopping cart'
#         ),
#     ],
#     user_id: str = Depends(validate_object_id),
# ):
#     if isinstance(data_items_update.price, Decimal):
#         # Configurar a precisão das operações decimais para 10 dígitos
#         getcontext().prec = 10

#         data_items_update.price = str(
#             data_items_update.price.quantize(Decimal('0.01'), ROUND_DOWN)
#         )

#     filter_document_pull = {
#         'user_id': ObjectId(user_id),
#         'shoppingCart.category_value': category_value,
#         'shoppingCart.items.item_id': item_id,
#     }

#     # Remover o item
#     request_pull = {
#         '$pull': {'shoppingCart.$[element].items': {'item_id': item_id}}
#     }

#     array_filters_pull = [
#         {'element.category_value': category_value},
#     ]

#     # Executar a remoção do item
#     pull_result = await collection_repository.update_document(
#         filter_document=filter_document_pull,
#         request_attribute=request_pull,
#         array_filters=array_filters_pull,
#     )

#     if pull_result.modified_count == 0:
#         raise HTTPException(
#             status_code=status.HTTP_304_NOT_MODIFIED,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL,
#                 msg='The item was not found or was not removed',
#             ).model_dump(),
#         )

#     filter_document_add_to_set = {
#         'user_id': ObjectId(user_id),
#         'shoppingCart.category_value': category_value,
#     }

#     # adiciona o item atualizado
#     request_push = {
#         '$addToSet': {
#             'shoppingCart.$.items': {
#                 'item_id': item_id,
#                 **data_items_update.model_dump(),
#             }
#         }
#     }

#     # Executar a adição do item atualizado
#     add_to_set_result = await collection_repository.update_document(
#         filter_document=filter_document_add_to_set,
#         request_attribute=request_push,
#     )

#     if add_to_set_result.modified_count == 0:
#         raise HTTPException(
#             status_code=status.HTTP_304_NOT_MODIFIED,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='Item not modified'
#             ).model_dump(),
#         )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS, msg='Item updated successfully'
#     ).model_dump()


# async def create_shopping_cart(user_id: ObjectId, username: str):
#     shopping_cart_model = get_default_pantry_model(user_id, username)

#     await collection_repository.insert_document(shopping_cart_model)


# async def update_username_shopping_cart(user_id: str, username: str):
#     filter_document = {'user_id': ObjectId(user_id)}

#     request_attribute = {'$set': {'username': username}}

#     await collection_repository.update_document(
#         filter_document, request_attribute
#     )


# async def delete_db_shopping_cart():
#     collection_repository.delete_many()

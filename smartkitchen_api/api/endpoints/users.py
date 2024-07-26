from beanie import PydanticObjectId
from beanie.operators import Or, Set
from bson import ObjectId
from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

# from smartkitchen_api.api.endpoints.pantry import (
#     create_categories,
#     update_username_pantry,
# # )
# from smartkitchen_api.api.endpoints.shopping_cart import (
#     create_shopping_cart,
#     update_username_shopping_cart,
# )
# from smartkitchen_api.api.schema.default_answer import (
# DefaultAnswer,StatusMsg
# )
# from smartkitchen_api.api.schema.users import UserIn, UserInUpdate, UserOut
# from smartkitchen_api.middleware.validate_object_id import validate_object_id
# from smartkitchen_api.models.connection_options.mongo_db_config import (
#     mongo_db_infos,
# )
# from smartkitchen_api.models.open_connection import open_connection
from smartkitchen_api.models.pantry import Categories, Pantry, pantry_data
from smartkitchen_api.models.user import UpdateUser, User

router = APIRouter()

# collection_repository = open_connection(
#     mongo_db_infos['COLLECTIONS']['collection_users']  # type: ignore
# )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def create_new_user(user: User):
    username_exist = await user.find(
        Or(
            User.username == user.username,
            User.email == user.email,
        )
    ).first_or_none()

    if username_exist:
        if username_exist.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O nome de usuário já existe',
            )
        elif username_exist.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O e-mail já existe',
            )

    await user.insert()

    user_pantry = Pantry(
        user_id=ObjectId(user.id),
        username=user.username,
        pantry=[Categories(**cat) for cat in pantry_data],
    )

    await user_pantry.insert()

    return user


@router.put('/', status_code=status.HTTP_200_OK, response_model=User)
async def update_user(user_id: PydanticObjectId, update_user: UpdateUser):
    user = await User.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O usuário não foi encontrado.',
        )

    # REMOVE OS CAMPOS COM VALORES ´NONE´
    update_user_data = update_user.model_dump(exclude_none=True)

    await user.update(Set(update_user_data))

    user = await User.get(user_id)

    return user


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: PydanticObjectId):
    user = await User.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O usuário não foi encontrado',
        )

    await user.delete()


# @router.get('/', response_model=DefaultAnswer,
# status_code=status.HTTP_200_OK)
# async def read_users():
#     request_attribute = {'_id': 0, 'password': 0}

#     data = await collection_repository.find_document(
#         request_attribute=request_attribute
#     )

#     if not data:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='Users not found'
#             ).model_dump(),
#         )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS, msg='Users found', data=data
#     )


# @router.get(
#    '/{user_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def read_user(user_id: str = Depends(validate_object_id)):
#     filter_document = {'_id': ObjectId(user_id)}
#     request_attribute = {'_id': 0, 'password': 0}

#     data = await collection_repository.find_document_one(
#         filter_document, request_attribute
#     )

#     if not data:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='User not found'
#             ).model_dump(),
#         )

#     return DefaultAnswer(status=StatusMsg.SUCCESS, msg='User found', data=data)


# @router.post(
#     '/', response_model=DefaultAnswer, status_code=status.HTTP_201_CREATED
# )
# async def create_user(new_user: UserIn):
#     data_user = new_user.model_dump()

#     filter_document_username = {'username': data_user['username']}
#     filter_document_email = {'email': data_user['email']}
#     request_attribute = {'_id': 0, 'password': 0}

#     does_the_username_exist = await collection_repository.find_document(
#         filter_document_username, request_attribute
#     )

#     does_the_email_exist = await collection_repository.find_document(
#         filter_document_email, request_attribute
#     )

#     if does_the_email_exist or does_the_username_exist:
#         msg = (
#             'username and email already exists'
#             if does_the_email_exist and does_the_username_exist
#             else 'username already exists'
#             if does_the_username_exist
#             else 'This email already exists'
#         )
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail=DefaultAnswer(status=StatusMsg.FAIL, msg=msg).model_dump(),
#         )

#     insert_one_result = await collection_repository.insert_document(data_user)

#     data = [
#         UserOut(
#             username=data_user['username'], email=data_user['email']
#         ).model_dump()
#     ]

#     # TODO: As criações de categorias e carrinho de compras
#     #  precisão ser somente chamadas se o usuário for criado ?
#     #  precisa haver algum tipo de validação para elas
#     #  serem chamadas ?
#     await create_categories(
#         user_id=insert_one_result.inserted_id, username=data_user['username']
#     )

#     await create_shopping_cart(
#         user_id=insert_one_result.inserted_id, username=data_user['username']
#     )

#     return DefaultAnswer(
#         status=StatusMsg.SUCCESS, msg='User created', data=data
#     )


# @router.delete(
#     '/{user_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def del_document(user_id: str = Depends(validate_object_id)):
#     # TODO Devo chamar uma função aqui também que deleta o DB
#     #  pantry do usuário porque e se ele quiser voltar
#     #  a usar o App?

#     filter_document = {'_id': ObjectId(user_id)}

#     delete_result = await collection_repository.delete_document(
#         filter_document
#     )

#     if not delete_result.deleted_count:
#         response = DefaultAnswer(
#             status=StatusMsg.FAIL, msg='user not found'
#         ).model_dump()
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT, detail=response
#         )

#     return DefaultAnswer(status=StatusMsg.SUCCESS, msg='User deleted')


# @router.put(
#     '/{user_id}', response_model=DefaultAnswer, status_code=status.HTTP_200_OK
# )
# async def update_document(
#     data_user_update: UserInUpdate, user_id: str = Depends(validate_object_id)
# ):
#     # TODO: Se você passar um usuário inexistente, ele tenta validar primeiro a os campos de usuário e senha para depois tentar ver se o usuário existe  # noqa: E501

#     # TODO: Faz sentido esses updates estarem na mesma rota no caso eu deveria criar rotas para cada attr do usuário a ser atualizado.  # noqa: E501

#     # TODO: Precisa criar o método de atualizar o user name da collection pantry também  # noqa: E501

#     filter_document = {'_id': ObjectId(user_id)}

#     # Verifica se o usuário existe
#     existing_user = await collection_repository.find_document_one(
#         filter_document
#     )
#     if not existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='User not found'
#             ).model_dump(),
#         )

#     # Verifica se o username já está em uso
#     if (
#         data_user_update.username
#         and await collection_repository.find_document_one({
#             'username': data_user_update.username
#         })
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='Username already in use'
#             ).model_dump(),
#         )

#     # Verifica se o email já está em uso
#     if (
#         data_user_update.email
#         and await collection_repository.find_document_one({
#             'email': data_user_update.email
#         })
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='Email already in use'
#             ).model_dump(),
#         )

#     # Removendo os attr com valores None
#     request_attribute = {
#         '$set': data_user_update.model_dump(exclude_unset=True)
#     }

#     # Atualiza o documento no MongoDB
#     update_result = await collection_repository.update_document(
#         filter_document=filter_document, request_attribute=request_attribute
#     )

#     if update_result.modified_count == 1:
#         # TODO: Após atualizado o usuário, no caso do username ele atualiza na collection pantry. Nesse caso ele vai atualizar mesmo que nome se a que ele já em lá logo preciso mudar essa func de lugar.  # noqa: E501
#         if data_user_update.username:
#             await update_username_pantry(user_id, data_user_update.username)
#             await update_username_shopping_cart(
#                 user_id, data_user_update.username
#             )

#         return DefaultAnswer(
#             status=StatusMsg.SUCCESS, msg='User updated successfully'
#         ).model_dump()
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_304_NOT_MODIFIED,
#             detail=DefaultAnswer(
#                 status=StatusMsg.FAIL, msg='User not modified'
#             ).model_dump(),
#         )


# async def delete_all_users():
#     collection_repository.delete_many()

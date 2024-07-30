from typing import List

from beanie import PydanticObjectId
from beanie.operators import Or, Set
from fastapi import APIRouter, Body, HTTPException, status

from smartkitchien_api.models.user import User, UserPublic, UserUpdate, user_example

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserPublic])
async def read_users():
    users = await User.find().to_list()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Nenhum usuário foi encontrado',
        )

    return users


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user(user_id: PydanticObjectId):
    user = await User.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O usuário não foi encontrado',
        )

    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_new_user(
    user: User = Body(example=user_example),
):
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

    return UserPublic(**user.model_dump())


@router.put('/', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user(
    user_id: PydanticObjectId,
    update_user: UserUpdate = Body(example=user_example),
):
    user = await User.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='O usuário não foi encontrado.',
        )

    if user:
        if user.username == update_user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O nome de usuário já existe',
            )
        elif user.email == update_user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O e-mail já existe',
            )

    # REMOVE OS CAMPOS COM VALORES ´NONE´
    update_user_data = update_user.model_dump(exclude_none=True)

    await user.update(Set(update_user_data))

    return UserPublic(**user.model_dump())


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

from typing import Annotated, List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.models.user import User, UserPublic
from smartkitchien_api.security.security import get_current_user

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


@router.get('/me', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Você não tem permissão.'
        )

    return current_user
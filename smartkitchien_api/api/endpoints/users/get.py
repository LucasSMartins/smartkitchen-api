from typing import Annotated, List

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.user import User, UserPublic
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserPublic])
async def read_users():
    users = await User.find().to_list()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
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
    check_user_permission(current_user.id, user_id)  # type: ignore

    return current_user

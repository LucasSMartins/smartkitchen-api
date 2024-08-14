from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.users import InformationUsers
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.user import User, UserPublic
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/', status_code=status.HTTP_200_OK, response_model=DefaultAnswer)
async def read_users():
    users = await User.find().to_list()

    if not users:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationUsers.USER_NOT_FOUND['title'],
            msg=InformationUsers.USER_NOT_FOUND['msg'],
            loc=InformationUsers.USER_NOT_FOUND['loc'],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_FOUND['title'],
        msg=InformationUsers.USER_FOUND['msg'],
    )

    return DefaultAnswer(detail=detail)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=User)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def read_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    return current_user

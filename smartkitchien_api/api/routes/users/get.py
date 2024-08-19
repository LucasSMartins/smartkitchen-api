from site import USER_BASE
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.users import InformationUsers
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.user import User, UserPublic, response_200_example
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=DefaultAnswer,
    description=response_200_example,
)
async def read_users():
    users = await User.find().to_list()

    if not users:
        detail_error = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationUsers.USER_NOT_FOUND['title'],
            msg=InformationUsers.USER_NOT_FOUND['msg'],
            loc=InformationUsers.USER_NOT_FOUND['loc'],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error.model_dump(),
        )

    users_public = [UserPublic(**user.model_dump()) for user in users]

    detail_success = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_FOUND['title'],
        msg=InformationUsers.USER_FOUND['msg'],
        data=users_public,
    )

    return DefaultAnswer(detail=detail_success)


@router.get('/me', status_code=status.HTTP_200_OK, response_model=DefaultAnswer)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    detail_success = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_FOUND['title'],
        msg=InformationUsers.USER_FOUND['msg'],
        data=UserPublic(**current_user.model_dump()),
    )

    return DefaultAnswer(detail=detail_success)


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=DefaultAnswer)
async def read_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    detail_success = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_FOUND['title'],
        msg=InformationUsers.USER_FOUND['msg'],
        data=UserPublic(**current_user.model_dump()),
    )

    return DefaultAnswer(detail=detail_success)

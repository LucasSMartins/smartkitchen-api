from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from smartkitchen_api.messages.users import InformationUsers
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


@router.delete(
    '/{user_id}', status_code=status.HTTP_200_OK, response_model=DefaultAnswer
)
async def delete_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    await current_user.delete()

    detail_success = [
        AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationUsers.USER_DELETED['title'],
            msg=InformationUsers.USER_DELETED['msg'],
        )
    ]

    return DefaultAnswer(detail=detail_success)

from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import Set
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchen_api.messages.users import InformationUsers
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.user import User, UserUpdate, user_example
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user, get_password_hash

router = APIRouter()


@router.put(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=DefaultAnswer,
)
async def update_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
    update_user: UserUpdate = Body(example=user_example),
):
    check_user_permission(current_user.id, user_id)

    username_exist = await User.get(user_id)

    if username_exist:
        if username_exist.username == update_user.username:
            detail = AnswerDetail(
                status=status.HTTP_409_CONFLICT,
                type=TypeAnswers.CONFLICT,
                title=InformationUsers.USERNAME_ALREADY_EXISTS['title'],
                msg=InformationUsers.USERNAME_ALREADY_EXISTS['msg'],
                loc=InformationUsers.USERNAME_ALREADY_EXISTS['loc'],
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail.model_dump(),
            )
        elif username_exist.email == update_user.email:
            detail = AnswerDetail(
                status=status.HTTP_409_CONFLICT,
                type=TypeAnswers.CONFLICT,
                title=InformationUsers.EMAIL_ALREADY_EXISTS['title'],
                msg=InformationUsers.EMAIL_ALREADY_EXISTS['msg'],
                loc=InformationUsers.EMAIL_ALREADY_EXISTS['loc'],
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail.model_dump(),
            )

    if update_user.password:
        update_user.password = get_password_hash(update_user.password)

    # REMOVE OS CAMPOS COM VALORES ´None´
    update_user_data = update_user.model_dump(exclude_none=True)

    await current_user.update(Set(update_user_data))

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_UPDATED['title'],
        msg=InformationUsers.USER_UPDATED['msg'],
    )

    return DefaultAnswer(detail=detail)

from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.pantry import InformationPantry
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import Pantry, PantryPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=AnswerDetail,
)
async def read_user_pantry(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()

    detail_error = AnswerDetail(
        status=status.HTTP_404_NOT_FOUND,
        type=TypeAnswers.NOT_FOUND,
        title=InformationPantry.PANTRY_NOT_FOUND['title'],
        msg=InformationPantry.PANTRY_NOT_FOUND['msg'],
        loc=InformationPantry.PANTRY_NOT_FOUND['loc'],
    )

    if user_pantry:
        detail_success = AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationPantry.PANTRY_FOUND['title'],
            msg=InformationPantry.PANTRY_FOUND['msg'],
            data=PantryPublic(**user_pantry.model_dump()),
        )

    if not user_pantry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error.model_dump(),
        )

    return DefaultAnswer(detail=detail_success)

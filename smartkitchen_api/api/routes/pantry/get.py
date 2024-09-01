from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchen_api.messages.pantry import InformationPantry
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.pantry import Pantry, PantryPublic
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=DefaultAnswer,
)
async def read_user_pantry(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()

    detail_error = [
        AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationPantry.PANTRY_NOT_FOUND['title'],
            msg=InformationPantry.PANTRY_NOT_FOUND['msg'],
            loc=InformationPantry.PANTRY_NOT_FOUND['loc'],
        ).model_dump()
    ]

    if not user_pantry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail_error)
    else:
        detail_success = [
            AnswerDetail(
                status=status.HTTP_200_OK,
                type=TypeAnswers.SUCCESS,
                title=InformationPantry.PANTRY_FOUND['title'],
                msg=InformationPantry.PANTRY_FOUND['msg'],
                data=PantryPublic(**user_pantry.model_dump()),
            )
        ]

    return DefaultAnswer(detail=detail_success)

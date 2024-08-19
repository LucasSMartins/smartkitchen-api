from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.cookbook import InformationCookbook
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.cookbook import Cookbook, CookbookPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=DefaultAnswer)
async def read_user_cookbook(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_cookbook = await Cookbook.find(Cookbook.user_id == user_id).first_or_none()

    detail_error = AnswerDetail(
        status=status.HTTP_404_NOT_FOUND,
        type=TypeAnswers.NOT_FOUND,
        title=InformationCookbook.COOKBOOK_NOT_FOUND['title'],
        msg=InformationCookbook.COOKBOOK_NOT_FOUND['msg'],
        loc=InformationCookbook.COOKBOOK_NOT_FOUND['loc'],
    )

    if not user_cookbook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail_error.model_dump()
        )
    else:
        detail_success = AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationCookbook.COOKBOOK_FOUND['title'],
            msg=InformationCookbook.COOKBOOK_FOUND['msg'],
            data=CookbookPublic(**user_cookbook.model_dump()),
        )

    return DefaultAnswer(detail=detail_success)

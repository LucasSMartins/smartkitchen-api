from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.messages.pantry import InformationPantry
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import (
    Pantry,
    PantryPublic,
    item_with_price,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.enums.category_value import (
    CategoryValue,
    category_description,
)
from smartkitchien_api.schema.items import ItemsUpdate
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.put(
    '/{user_id}item/{item_id}/category/{category_value}',
    status_code=status.HTTP_200_OK,
    description=category_description,
    response_model=DefaultAnswer,
)
async def update_item_pantry(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item_update: ItemsUpdate = Body(
        example=item_with_price,
    ),
):
    check_user_permission(current_user.id, user_id)

    user_pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()

    if not user_pantry:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationPantry.PANTRY_NOT_FOUND['title'],
            msg=InformationPantry.PANTRY_NOT_FOUND['msg'],
            loc=InformationPantry.PANTRY_NOT_FOUND['loc'],
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    category_found = False
    item_found = False

    for category in user_pantry.pantry:
        if category.category_value == category_value:
            category_found = True
            for item in category.items:
                if item.id == item_id:
                    update_data = item_update.model_dump(exclude_none=True)
                    for key, value in update_data.items():
                        setattr(item, key, value)
                    item_found = True
                    break
            if item_found:
                break

    if not category_found:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationPantry.CATEGORY_NOT_FOUND['title'],
            msg=InformationPantry.CATEGORY_NOT_FOUND['msg'],
            loc=InformationPantry.CATEGORY_NOT_FOUND['loc'],
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    if not item_found:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationPantry.ITEM_NOT_FOUND['title'],
            msg=InformationPantry.ITEM_NOT_FOUND['msg'],
            loc=InformationPantry.ITEM_NOT_FOUND['loc'],
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    await user_pantry.save()

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationPantry.PANTRY_FOUND['title'],
        msg=InformationPantry.PANTRY_FOUND['msg'],
        data=PantryPublic(**user_pantry.model_dump()),
    )

    return DefaultAnswer(detail=detail)

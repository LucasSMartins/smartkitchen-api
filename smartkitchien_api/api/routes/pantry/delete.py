from typing import Annotated

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.pantry import InformationPantry
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.categories import CategoryValue
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.delete(
    '/{user_id}/item/{item_id}/category/{category_value}',
    status_code=status.HTTP_200_OK,
    response_model=DefaultAnswer,
)
async def delete_item(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
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

    # Procura o item e remove-o da categoria correspondente
    category_found = False
    for category in user_pantry.pantry:
        if category.category_value == category_value:
            category_found = True
            item_found = False
            for item in category.items:
                if item.id == ObjectId(item_id):
                    category.items.remove(item)
                    item_found = True
                    break

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

            # Remove a categoria se não houver itens
            if not category.items:
                user_pantry.pantry.remove(category)
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

    # Salva e se a dispensa estiver vazia o exclui.
    await user_pantry.save()

    if not user_pantry.pantry:
        await user_pantry.delete()

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationPantry.ITEM_DELETED['title'],
        msg=InformationPantry.ITEM_DELETED['msg'],
    )

    return DefaultAnswer(detail=detail)

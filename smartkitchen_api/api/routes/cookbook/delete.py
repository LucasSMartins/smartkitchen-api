from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchen_api.messages.cookbook import InformationCookbook
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.cookbook import Cookbook
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.enums.category_value import CategoryValue
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


@router.delete(
    '/{user_id}/recipe/{recipe_id}/category/{category_value}',
    status_code=status.HTTP_200_OK,
    response_model=DefaultAnswer,
)
async def delete_user_cookbook(
    user_id: PydanticObjectId,
    recipe_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_cookbook = await Cookbook.find(Cookbook.user_id == user_id).first_or_none()

    if not user_cookbook:
        detail_error = [
            AnswerDetail(
                status=status.HTTP_404_NOT_FOUND,
                type=TypeAnswers.NOT_FOUND,
                title=InformationCookbook.CATEGORY_NOT_FOUND['title'],
                msg=InformationCookbook.CATEGORY_NOT_FOUND['msg'],
                loc=InformationCookbook.CATEGORY_NOT_FOUND['loc'],
            ).model_dump()
        ]

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error,
        )

    # Procura o item e remove-o da categoria correspondente
    category_found = False
    for category in user_cookbook.cookbook:
        if category.category_value == category_value:
            category_found = True
            recipe_found = False
            for recipe in category.items:
                if recipe.id == recipe_id:
                    category.items.remove(recipe)
                    recipe_found = True
                    break

            if not recipe_found:
                detail_error = [
                    AnswerDetail(
                        status=status.HTTP_404_NOT_FOUND,
                        type=TypeAnswers.NOT_FOUND,
                        title=InformationCookbook.RECIPE_NOT_FOUND['title'],
                        msg=InformationCookbook.RECIPE_NOT_FOUND['msg'],
                        loc=InformationCookbook.RECIPE_NOT_FOUND['loc'],
                    ).model_dump()
                ]

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail_error
                )

            # Remove a categoria se não houver itens
            if not category.items:
                user_cookbook.cookbook.remove(category)
            break

    if not category_found:
        detail_error = [
            AnswerDetail(
                status=status.HTTP_404_NOT_FOUND,
                type=TypeAnswers.NOT_FOUND,
                title=InformationCookbook.CATEGORY_NOT_FOUND['title'],
                msg=InformationCookbook.CATEGORY_NOT_FOUND['msg'],
                loc=InformationCookbook.CATEGORY_NOT_FOUND['loc'],
            ).model_dump()
        ]

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail_error)

    await user_cookbook.save()

    if not user_cookbook.cookbook:
        await user_cookbook.delete()

    detail_success = [
        AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationCookbook.RECIPE_DELETED['title'],
            msg=InformationCookbook.RECIPE_DELETED['msg'],
        )
    ]

    return DefaultAnswer(detail=detail_success)

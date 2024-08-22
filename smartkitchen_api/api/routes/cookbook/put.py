from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchen_api.messages.cookbook import InformationCookbook
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.cookbook import Cookbook
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.enums.category_value import (
    CategoryValue,
    category_description,
)
from smartkitchen_api.schema.recipe import RecipeUpdate
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


@router.put(
    '/{user_id}/recipe/{recipe_id}/category/{category_value}',
    status_code=status.HTTP_200_OK,
    description=category_description,
    response_model=DefaultAnswer,
)
async def update_item_cookbook(
    user_id: PydanticObjectId,
    recipe_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    recipe_update: RecipeUpdate,
):
    check_user_permission(current_user.id, user_id)

    user_cookbook = await Cookbook.find(Cookbook.user_id == user_id).first_or_none()

    if not user_cookbook:
        detail_error = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationCookbook.COOKBOOK_NOT_FOUND['title'],
            msg=InformationCookbook.COOKBOOK_NOT_FOUND['msg'],
            loc=InformationCookbook.COOKBOOK_NOT_FOUND['loc'],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error.model_dump(),
        )

    category_found = False
    recipe_found = False

    for category in user_cookbook.cookbook:
        if category.category_value == category_value:
            category_found = True

            for recipe in category.items:
                if recipe.id == recipe_id:
                    update_data = recipe_update.model_dump(exclude_none=True)
                    for key, value in update_data.items():
                        setattr(recipe, key, value)

                    recipe_found = True
                    break

            if recipe_found:
                break

    if not category_found:
        detail_error = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationCookbook.CATEGORY_NOT_FOUND['title'],
            msg=InformationCookbook.CATEGORY_NOT_FOUND['msg'],
            loc=InformationCookbook.CATEGORY_NOT_FOUND['loc'],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error.model_dump(),
        )

    if not recipe_found:
        detail_error = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationCookbook.RECIPE_NOT_FOUND['title'],
            msg=InformationCookbook.RECIPE_NOT_FOUND['msg'],
            loc=InformationCookbook.RECIPE_NOT_FOUND['loc'],
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail_error.model_dump(),
        )

    await user_cookbook.save()

    detail_success = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationCookbook.RECIPE_UPDATED['title'],
        msg=InformationCookbook.RECIPE_UPDATED['msg'],
    )

    return DefaultAnswer(detail=detail_success)

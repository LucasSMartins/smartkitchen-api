from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchen_api.messages.cookbook import InformationCookbook
from smartkitchen_api.messages.generic import InformationGeneric
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.cookbook import Cookbook, recipe_example
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.categories import Categories, CategoryValue
from smartkitchen_api.schema.enums.category_value import category_description
from smartkitchen_api.schema.recipe import Recipe
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


async def create_category(
    current_user_cookbook: Cookbook, category_value: CategoryValue
):
    if not any(
        category.category_value == category_value
        for category in current_user_cookbook.cookbook
    ):
        current_user_cookbook.cookbook.append(
            Categories(category_value=category_value, category_name=category_value.name)
        )
        await current_user_cookbook.save()


async def add_item_to_list(
    current_user_cookbook: Cookbook, category_value: CategoryValue, recipe: Recipe
):
    for category in current_user_cookbook.cookbook:
        if category.category_value == category_value:
            category.items.append(recipe)

            await current_user_cookbook.save()

            return

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


async def get_collection(current_user_id: PydanticObjectId):
    try:
        cookbook_collection = await Cookbook.find(
            Cookbook.user_id == current_user_id,
        ).first_or_none()

        return cookbook_collection

    except PyMongoError as e:
        # TODO: Log ou exiba uma mensagem de erro apropriada
        print(f'Erro ao consultar o banco de dados: {e}')
        # Ou lançar uma exceção personalizada se necessário
        detail_error = [
            AnswerDetail(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                type=TypeAnswers.INTERNAL_SERVER_ERROR,
                title=InformationGeneric.INTERNAL_SERVER_ERROR['title'],
                msg=InformationGeneric.INTERNAL_SERVER_ERROR['msg'],
                loc=InformationGeneric.INTERNAL_SERVER_ERROR['loc'],
            ).model_dump()
        ]

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail_error
        )


@router.post(
    '/{user_id}/category/{category_value}',
    status_code=status.HTTP_201_CREATED,
    description=category_description,
    response_model=DefaultAnswer,
)
async def create_recipe(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    recipe: Recipe = Body(example=recipe_example),
):
    check_user_permission(current_user.id, user_id)

    cookbook_collection = await get_collection(user_id)

    if not cookbook_collection:
        user_cookbook_collection = await Cookbook(
            user_id=current_user.id,
            cookbook=[
                Categories(
                    category_value=category_value,
                    category_name=category_value.name,
                )
            ],
        ).insert()

        await add_item_to_list(user_cookbook_collection, category_value, recipe)

    else:
        await create_category(cookbook_collection, category_value)

        await add_item_to_list(cookbook_collection, category_value, recipe)

    detail_success = [
        AnswerDetail(
            status=status.HTTP_201_CREATED,
            type=TypeAnswers.SUCCESS,
            title=InformationCookbook.COOKBOOK_CREATED['title'],
            msg=InformationCookbook.COOKBOOK_CREATED['msg'],
        )
    ]

    return DefaultAnswer(detail=detail_success)

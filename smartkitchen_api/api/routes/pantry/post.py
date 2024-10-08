from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchen_api.messages.generic import InformationGeneric
from smartkitchen_api.messages.pantry import InformationPantry
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.pantry import (
    Pantry,
    item_description,
    item_with_price,
    item_without_price,
)
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.categories import Categories
from smartkitchen_api.schema.enums.category_value import (
    CategoryValue,
    category_description,
)
from smartkitchen_api.schema.items import Items
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


async def create_category(current_user_pantry: Pantry, category_value: CategoryValue):
    if not any(
        category.category_value == category_value
        for category in current_user_pantry.pantry
    ):
        current_user_pantry.pantry.append(
            Categories(category_value=category_value, category_name=category_value.name)
        )
        await current_user_pantry.save()


async def add_item_to_list(
    current_user_pantry: Pantry, category_value: CategoryValue, item: Items
):
    for category in current_user_pantry.pantry:
        if category.category_value == category_value:
            # Verifica se já existe um item com o mesmo nome,
            # Se algum valor da lista for verdadeiro (true) a função Any retorna True
            if any(existing_item.name == item.name for existing_item in category.items):
                detail_error = [
                    AnswerDetail(
                        status=status.HTTP_409_CONFLICT,
                        type=TypeAnswers.CONFLICT,
                        title=InformationPantry.ITEM_ALREADY_EXISTS['title'],
                        msg=InformationPantry.ITEM_ALREADY_EXISTS['msg'],
                        loc=InformationPantry.ITEM_ALREADY_EXISTS['loc'],
                    ).model_dump()
                ]

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail=detail_error
                )

            category.items.append(item)

            await current_user_pantry.save()

            return

    detail_error = [
        AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationPantry.CATEGORY_NOT_FOUND['title'],
            msg=InformationPantry.CATEGORY_NOT_FOUND['msg'],
            loc=InformationPantry.CATEGORY_NOT_FOUND['loc'],
        ).model_dump()
    ]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail_error,
    )


async def get_pantry_collection(user_id: PydanticObjectId):
    try:
        pantry_collection = await Pantry.find(
            Pantry.user_id == user_id,
        ).first_or_none()

        return pantry_collection

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
async def create_item_pantry(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item: Items = Body(
        examples=[item_with_price, item_without_price],
        description=item_description,
    ),
):
    check_user_permission(current_user.id, user_id)

    pantry_collection = await get_pantry_collection(user_id)

    if not pantry_collection:
        # Cria o um Document Pantry na collection pantry.
        user_pantry_collection = await Pantry(
            user_id=current_user.id,
            pantry=[
                Categories(
                    category_value=category_value, category_name=category_value.name
                )
            ],
        ).insert()

        await add_item_to_list(user_pantry_collection, category_value, item)

    else:
        await create_category(pantry_collection, category_value)

        await add_item_to_list(pantry_collection, category_value, item)

    detail_success = [
        AnswerDetail(
            status=status.HTTP_201_CREATED,
            type=TypeAnswers.SUCCESS,
            title=InformationPantry.PANTRY_CREATED['title'],
            msg=InformationPantry.PANTRY_CREATED['msg'],
        )
    ]

    return DefaultAnswer(detail=detail_success)

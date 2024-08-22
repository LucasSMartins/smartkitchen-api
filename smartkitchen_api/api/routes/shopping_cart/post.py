from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchen_api.messages.generic import InformationGeneric
from smartkitchen_api.messages.shopping_cart import InformationShoppingCart
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.shopping_cart import (
    ShoppingCart,
    item_description,
    item_with_price,
    item_without_price,
)
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.categories import (
    Categories,
)
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


async def create_category(
    current_user_shopping_cart: ShoppingCart, category_value: CategoryValue
):
    if not any(
        category.category_value == category_value
        for category in current_user_shopping_cart.shopping_cart
    ):
        current_user_shopping_cart.shopping_cart.append(
            Categories(category_value=category_value, category_name=category_value.name)
        )
        await current_user_shopping_cart.save()


async def add_item_to_list(
    current_user_shopping_cart: ShoppingCart, category_value: CategoryValue, item: Items
):
    for category in current_user_shopping_cart.shopping_cart:
        if category.category_value == category_value:
            # Verifica se já existe um item com o mesmo nome,
            # Se algum valor da lista for verdadeiro (true) a função Any retorna True
            if any(existing_item.name == item.name for existing_item in category.items):
                detail = AnswerDetail(
                    status=status.HTTP_409_CONFLICT,
                    type=TypeAnswers.CONFLICT,
                    title=InformationShoppingCart.ITEM_ALREADY_EXISTS['title'],
                    msg=InformationShoppingCart.ITEM_ALREADY_EXISTS['msg'],
                    loc=InformationShoppingCart.ITEM_ALREADY_EXISTS['loc'],
                )
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=detail.model_dump(),
                )

            category.items.append(item)

            await current_user_shopping_cart.save()

            return

    detail = AnswerDetail(
        status=status.HTTP_404_NOT_FOUND,
        type=TypeAnswers.NOT_FOUND,
        title=InformationShoppingCart.CATEGORY_NOT_FOUND['title'],
        msg=InformationShoppingCart.CATEGORY_NOT_FOUND['msg'],
        loc=InformationShoppingCart.CATEGORY_NOT_FOUND['loc'],
    )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail.model_dump(),
    )


async def get_shopping_cart_collection(current_user_id: PydanticObjectId):
    try:
        shopping_cart_collection = await ShoppingCart.find(
            ShoppingCart.user_id == current_user_id,
        ).first_or_none()
        return shopping_cart_collection
    except PyMongoError as e:
        # TODO: Log ou exiba uma mensagem de erro apropriada
        print(f'Erro ao consultar o banco de dados: {e}')
        # Ou lançar uma exceção personalizada se necessário
        detail = AnswerDetail(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            type=TypeAnswers.INTERNAL_SERVER_ERROR,
            title=InformationGeneric.INTERNAL_SERVER_ERROR['title'],
            msg=InformationGeneric.INTERNAL_SERVER_ERROR['msg'],
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail.model_dump(),
        )


@router.post(
    '/{user_id}/category/{category_value}',
    status_code=status.HTTP_201_CREATED,
    description=category_description,
    response_model=DefaultAnswer,
)
async def create_item_shopping_cart(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item: Items = Body(
        examples=[item_with_price, item_without_price], description=item_description
    ),
):
    check_user_permission(current_user.id, user_id)

    shopping_cart_collection = await get_shopping_cart_collection(user_id)

    if not shopping_cart_collection:
        # Cria o um Document shopping_cart na collection shopping_cart.
        current_user_shopping_cart = await ShoppingCart(
            user_id=current_user.id,
            shopping_cart=[
                Categories(
                    category_value=category_value, category_name=category_value.name
                )
            ],
        ).insert()

        print(item)

        await add_item_to_list(current_user_shopping_cart, category_value, item)

    else:
        await create_category(shopping_cart_collection, category_value)

        await add_item_to_list(shopping_cart_collection, category_value, item)

    detail = AnswerDetail(
        status=status.HTTP_201_CREATED,
        type=TypeAnswers.SUCCESS,
        title=InformationShoppingCart.ITEM_ADDED['title'],
        msg=InformationShoppingCart.ITEM_ADDED['msg'],
    )

    return DefaultAnswer(detail=detail)

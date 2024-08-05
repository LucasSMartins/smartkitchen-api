from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.generic import GenericErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import (
    ShoppingCart,
    item_description,
    item_with_price,
    item_without_price,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.categories import (
    Categories,
)
from smartkitchien_api.schema.enums.category_value import (
    CategoryValue,
    category_description,
)
from smartkitchien_api.schema.items import Items
from smartkitchien_api.security.security import get_current_user

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
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=ErrorMessages.ITEM_ALREADY_EXISTS,
                )

            category.items.append(item)

            await current_user_shopping_cart.save()

            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=ErrorMessages.CATEGORY_NOT_FOUND,
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=GenericErrorMessages.INTERNAL_SERVER_ERROR_500,
        )


@router.post(
    '/{user_id}', status_code=status.HTTP_201_CREATED, description=category_description
)
async def create_item_shopping_cart(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item: Items = Body(
        examples=[item_with_price, item_without_price], description=item_description
    ),
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    shopping_cart_collection = await get_shopping_cart_collection(current_user.id)  # type: ignore

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

    return {'detail': SuccessMessages.ITEM_ADDED}

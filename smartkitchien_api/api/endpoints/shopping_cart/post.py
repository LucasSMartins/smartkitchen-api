from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.generic import GenericErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import (
    Categories,
    CategoryValue,
    Items,
    ShoppingCart,
    item_example,
)
from smartkitchien_api.models.user import User
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
            if any(
                existing_item.item_name == item.item_name
                for existing_item in category.items
            ):
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


@router.post('/{user_id}/item/{category}', status_code=status.HTTP_201_CREATED)
async def create_item_shopping_cart(
    user_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item: Items = Body(example=item_example),
):
    """
    **Lista dos valores de cada categoria de alimento**\n
    Pães e Produtos de Panificação = 101,\n
    Doces = 102,\n
    Produtos Enlatados e Conservas = 103,\n
    Materiais de Limpeza = 104,\n
    Condimentos e Molhos = 105,\n
    Laticínios e Ovos = 106,\n
    Bebidas = 107,\n
    Congelados = 108,\n
    Frutas e Vegetais = 109,\n
    Grãos e Cereais = 110,\n
    Produtos de Mercearia = 111,\n
    Lavanderia = 112,\n
    Carne e Peixe = 113,\n
    Massas e Produtos de Trigo = 114,\n
    Higiene Pessoal = 115,\n
    Temperos e Ervas Secas = 116,\n
    Papelaria = 117\n
    """

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

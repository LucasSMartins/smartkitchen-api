from typing import Annotated

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchen_api.messages.shopping_cart import InformationShoppingCart
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.shopping_cart import ShoppingCart
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.categories import CategoryValue
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

router = APIRouter()


@router.delete(
    '/{user_id}/item/{item_id}/category/{category_value}', response_model=DefaultAnswer
)
async def delete_item(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == user_id
    ).first_or_none()

    if not user_shopping_cart:
        detail_error = [
            AnswerDetail(
                status=status.HTTP_404_NOT_FOUND,
                type=TypeAnswers.NOT_FOUND,
                title=InformationShoppingCart.CART_NOT_FOUND['title'],
                msg=InformationShoppingCart.CART_NOT_FOUND['msg'],
                loc=InformationShoppingCart.CART_NOT_FOUND['loc'],
            ).model_dump(),
        ]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail_error)

    # Procura o item e remove-o da categoria correspondente
    category_found = False
    for category in user_shopping_cart.shopping_cart:
        if category.category_value == category_value:
            category_found = True
            item_found = False
            for item in category.items:
                if item.id == ObjectId(item_id):
                    category.items.remove(item)
                    item_found = True
                    break

            if not item_found:
                detail_error = [
                    AnswerDetail(
                        status=status.HTTP_404_NOT_FOUND,
                        type=TypeAnswers.NOT_FOUND,
                        title=InformationShoppingCart.ITEM_NOT_FOUND['title'],
                        msg=InformationShoppingCart.ITEM_NOT_FOUND['msg'],
                        loc=InformationShoppingCart.ITEM_NOT_FOUND['loc'],
                    ).model_dump(),
                ]

                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail_error
                )

            # Remove a categoria se não houver itens
            if not category.items:
                user_shopping_cart.shopping_cart.remove(category)
            break

    if not category_found:
        detail_error = [
            AnswerDetail(
                status=status.HTTP_404_NOT_FOUND,
                type=TypeAnswers.NOT_FOUND,
                title=InformationShoppingCart.CATEGORY_NOT_FOUND['title'],
                msg=InformationShoppingCart.CATEGORY_NOT_FOUND['msg'],
                loc=InformationShoppingCart.CATEGORY_NOT_FOUND['loc'],
            ).model_dump(),
        ]

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail_error)

    # Salva e, se necessário, exclui o carrinho de compras
    await user_shopping_cart.save()

    if not user_shopping_cart.shopping_cart:
        await user_shopping_cart.delete()

    detail_success = [
        AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationShoppingCart.ITEM_DELETED['title'],
            msg=InformationShoppingCart.ITEM_DELETED['msg'],
        )
    ]

    return DefaultAnswer(detail=detail_success)

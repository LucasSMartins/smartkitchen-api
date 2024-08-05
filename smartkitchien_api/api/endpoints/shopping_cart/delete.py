from typing import Annotated

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import ShoppingCart
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.categories import CategoryValue
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.delete('/')
async def delete_item(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == user_id
    ).first_or_none()

    if not user_shopping_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.SHOPPING_CART_NOT_FOUND,
        )

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
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessages.ITEM_NOT_FOUND,
                )

            # Remove a categoria se não houver itens
            if not category.items:
                user_shopping_cart.shopping_cart.remove(category)
            break

    if not category_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CATEGORY_NOT_FOUND,
        )

    # Salva e, se necessário, exclui a despensa
    await user_shopping_cart.save()

    if not user_shopping_cart.shopping_cart:
        await user_shopping_cart.delete()

    return {'detail': SuccessMessages.ITEM_DELETED}

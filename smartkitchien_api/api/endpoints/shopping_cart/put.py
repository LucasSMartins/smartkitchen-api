from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import (
    CategoryValue,
    ItemsUpdate,
    ShoppingCart,
    ShoppingCartPublic,
    item_example,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.put('/', status_code=status.HTTP_200_OK)
async def update_item_shopping_cart(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item_update: ItemsUpdate = Body(example=item_example),
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == user_id
    ).first_or_none()

    if not user_shopping_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PANTRY_NOT_FOUND,
        )

    # Procura o item e atualiza-o na categoria correspondente
    category_found = False
    item_found = False

    for category in user_shopping_cart.shopping_cart:
        if category.category_value == category_value:
            category_found = True
            for item in category.items:
                if item.id == item_id:
                    update_data = item_update.model_dump(exclude_none=True)
                    for key, value in update_data.items():
                        # ! ATENÇÃO se o attr não existir ele irá criar um.
                        setattr(item, key, value)
                    item_found = True
                    break
            if item_found:
                break

    if not category_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CATEGORY_NOT_FOUND,
        )

    if not item_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.ITEM_NOT_FOUND,
        )

    await user_shopping_cart.save()

    return ShoppingCartPublic(**user_shopping_cart.model_dump())

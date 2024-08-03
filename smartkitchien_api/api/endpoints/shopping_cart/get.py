from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import ShoppingCart, ShoppingCartPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_user_shopping_cart(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == current_user.id
    ).first_or_none()

    if not user_shopping_cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.SHOPPING_CART_NOT_FOUND,
        )

    user_user_shopping_cart_data = ShoppingCartPublic(**user_shopping_cart.model_dump())  # type: ignore

    return {'detail': user_user_shopping_cart_data}

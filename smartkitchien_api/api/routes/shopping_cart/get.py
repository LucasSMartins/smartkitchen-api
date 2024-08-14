from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.shopping_cart import InformationShoppingCart
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import ShoppingCart, ShoppingCartPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/{user_id}', status_code=status.HTTP_200_OK, response_model=DefaultAnswer)
async def read_user_shopping_cart(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)

    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == current_user.id
    ).first_or_none()

    if not user_shopping_cart:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationShoppingCart.CART_NOT_FOUND['title'],
            msg=InformationShoppingCart.CART_NOT_FOUND['msg'],
            loc=InformationShoppingCart.CART_NOT_FOUND['loc'],
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationShoppingCart.CART_FOUND['title'],
        msg=InformationShoppingCart.CART_FOUND['msg'],
        data=ShoppingCartPublic(**user_shopping_cart.model_dump()),
    )
    return DefaultAnswer(detail=detail)

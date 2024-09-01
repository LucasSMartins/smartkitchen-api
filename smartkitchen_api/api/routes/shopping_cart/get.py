from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchen_api.messages.shopping_cart import InformationShoppingCart
from smartkitchen_api.middleware.check_user_permission import check_user_permission
from smartkitchen_api.models.shopping_cart import ShoppingCart, ShoppingCartPublic
from smartkitchen_api.models.user import User
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_current_user

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

    detail_success = [
        AnswerDetail(
            status=status.HTTP_200_OK,
            type=TypeAnswers.SUCCESS,
            title=InformationShoppingCart.CART_FOUND['title'],
            msg=InformationShoppingCart.CART_FOUND['msg'],
            data=ShoppingCartPublic(**user_shopping_cart.model_dump()),
        )
    ]

    return DefaultAnswer(detail=detail_success)

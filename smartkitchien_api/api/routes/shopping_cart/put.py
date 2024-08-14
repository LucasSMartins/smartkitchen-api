from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.messages.shopping_cart import InformationShoppingCart
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.shopping_cart import (
    ShoppingCart,
    ShoppingCartPublic,
    item_with_price,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.categories import CategoryValue
from smartkitchien_api.schema.enums.category_value import category_description
from smartkitchien_api.schema.items import ItemsUpdate
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.put(
    '/{user_id}/item/{item_id}/category/{category_value}',
    status_code=status.HTTP_200_OK,
    description=category_description,
    response_model=DefaultAnswer,
)
async def update_item_shopping_cart(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item_update: ItemsUpdate = Body(
        example=item_with_price,
    ),
):
    check_user_permission(current_user.id, user_id)
    user_shopping_cart = await ShoppingCart.find(
        ShoppingCart.user_id == user_id
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

    if not item_found:
        detail = AnswerDetail(
            status=status.HTTP_404_NOT_FOUND,
            type=TypeAnswers.NOT_FOUND,
            title=InformationShoppingCart.ITEM_NOT_FOUND['title'],
            msg=InformationShoppingCart.ITEM_NOT_FOUND['msg'],
            loc=InformationShoppingCart.ITEM_NOT_FOUND['loc'],
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail.model_dump(),
        )

    await user_shopping_cart.save()

    detail = AnswerDetail(
        status=status.HTTP_200_OK,
        type=TypeAnswers.SUCCESS,
        title=InformationShoppingCart.ITEM_UPDATED['title'],
        msg=InformationShoppingCart.ITEM_UPDATED['msg'],
        data=ShoppingCartPublic(**user_shopping_cart.model_dump()),
    )

    return DefaultAnswer(detail=detail)

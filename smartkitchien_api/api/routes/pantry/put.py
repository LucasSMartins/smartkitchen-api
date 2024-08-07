from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import (
    Pantry,
    PantryPublic,
    item_with_price,
)
from smartkitchien_api.models.user import User
from smartkitchien_api.schema.enums.category_value import (
    CategoryValue,
    category_description,
)
from smartkitchien_api.schema.items import ItemsUpdate
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.put(
    '/{user_id}', status_code=status.HTTP_200_OK, description=category_description
)
async def update_item_pantry(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
    item_update: ItemsUpdate = Body(
        example=item_with_price,
    ),
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    user_pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()

    if not user_pantry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PANTRY_NOT_FOUND,
        )

    # Procura o item e atualiza-o na categoria correspondente
    category_found = False
    item_found = False

    for category in user_pantry.pantry:
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

    await user_pantry.save()

    return PantryPublic(**user_pantry.model_dump())

from typing import Annotated

from beanie import PydanticObjectId
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import CategoryValue, Pantry
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.delete('/')
async def delete_item(
    user_id: PydanticObjectId,
    item_id: PydanticObjectId,
    category_value: CategoryValue,
    current_user: Annotated[User, Depends(get_current_user)],
):
    # Verifica se o usuário tem permissão para realizar a ação
    check_user_permission(current_user.id, user_id)  # type: ignore

    # Encontra a despensa do usuário
    user_pantry = await Pantry.find(Pantry.user_id == user_id).first_or_none()

    if not user_pantry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PANTRY_NOT_FOUND,
        )

    # Procura o item e remove-o da categoria correspondente
    category_found = False
    for category in user_pantry.pantry:
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
                user_pantry.pantry.remove(category)
            break

    if not category_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.CATEGORY_NOT_FOUND,
        )

    # Salva e, se necessário, exclui a despensa
    await user_pantry.save()

    if not user_pantry.pantry:
        await user_pantry.delete()

    return {'detail': SuccessMessages.ITEM_DELETED}

from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.pantry import Pantry, PantryPublic
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.get('/{user_id}', status_code=status.HTTP_200_OK)
async def read_user_pantry(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    user_pantry = await Pantry.find(Pantry.user_id == current_user.id).first_or_none()

    if not user_pantry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.PANTRY_NOT_FOUND,
        )

    user_pantry_data = PantryPublic(**user_pantry.model_dump())  # type: ignore

    return {'detail': user_pantry_data}

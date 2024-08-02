from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    await current_user.delete()

    return {'detail': 'Usuário deletado com sucesso.'}

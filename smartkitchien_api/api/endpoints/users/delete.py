from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from smartkitchien_api.models.user import User
from smartkitchien_api.security.security import get_current_user

router = APIRouter()


@router.delete('/', status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Você não tem permissão para isso.',
        )

    await current_user.delete()

    return {'detail': 'Usuário deletado com sucesso.'}

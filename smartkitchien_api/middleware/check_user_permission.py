from beanie import PydanticObjectId
from fastapi import HTTPException, status


def check_user_permission(current_user_id: PydanticObjectId, user_id: PydanticObjectId):
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Você não tem permissão para isso.',
        )

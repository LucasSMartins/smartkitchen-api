from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import Or, Set
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.models.user import User, UserPublic, UserUpdate, user_example
from smartkitchien_api.security.security import get_current_user, get_password_hash

router = APIRouter()


@router.put('/', status_code=status.HTTP_200_OK, response_model=UserPublic)
async def update_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
    update_user: UserUpdate = Body(example=user_example),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Você não tem permissão para isso.',
        )

    username_exist = await User.find(
        Or(
            User.username == update_user.username,
            User.email == update_user.email,
        )
    ).first_or_none()

    if username_exist:
        if username_exist.username == update_user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O nome de usuário já existe',
            )
        elif username_exist.email == update_user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O e-mail já existe',
            )

    if update_user.password:
        update_user.password = get_password_hash(current_user.password)

    # REMOVE OS CAMPOS COM VALORES ´None´
    update_user_data = update_user.model_dump(exclude_none=True)

    await current_user.update(Set(update_user_data))

    return UserPublic(**current_user.model_dump())

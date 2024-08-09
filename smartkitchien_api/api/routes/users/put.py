from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import Set
from fastapi import APIRouter, Body, Depends, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.middleware.check_user_permission import check_user_permission
from smartkitchien_api.models.user import User, UserPublic, UserUpdate, user_example
from smartkitchien_api.security.security import get_current_user, get_password_hash

router = APIRouter()


@router.put(
    '/{user_id}', status_code=status.HTTP_200_OK, response_model=dict[str, UserPublic]
)
async def update_user(
    user_id: PydanticObjectId,
    current_user: Annotated[User, Depends(get_current_user)],
    update_user: UserUpdate = Body(example=user_example),
):
    check_user_permission(current_user.id, user_id)  # type: ignore

    username_exist = await User.get(user_id)

    if username_exist:
        if username_exist.username == update_user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.USERNAME_ALREADY_EXISTS,
            )
        elif username_exist.email == update_user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.EMAIL_ALREADY_EXISTS,
            )

    if update_user.password:
        update_user.password = get_password_hash(update_user.password)

    # REMOVE OS CAMPOS COM VALORES ´None´
    update_user_data = update_user.model_dump(exclude_none=True)

    await current_user.update(Set(update_user_data))

    update_user_public = UserPublic(**current_user.model_dump())

    return {'detail': update_user_public}

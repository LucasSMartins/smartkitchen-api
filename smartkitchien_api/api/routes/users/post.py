from beanie.operators import Or
from fastapi import APIRouter, Body, HTTPException, status

from smartkitchien_api.messages.error import ErrorMessages
from smartkitchien_api.messages.success import SuccessMessages
from smartkitchien_api.models.user import User, user_example
from smartkitchien_api.security.security import get_password_hash

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
)
async def create_new_user(
    user: User = Body(example=user_example),
):
    username_exist = await User.find(
        Or(
            User.username == user.username,
            User.email == user.email,
        )
    ).first_or_none()

    if username_exist:
        if username_exist.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.USERNAME_ALREADY_EXISTS_409,
            )
        elif username_exist.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=ErrorMessages.EMAIL_ALREADY_EXISTS_409,
            )

    user.password = get_password_hash(user.password)

    await user.insert()

    return {'detail': SuccessMessages.USER_CREATED}

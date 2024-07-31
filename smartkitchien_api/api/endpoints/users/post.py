from beanie.operators import Or
from fastapi import APIRouter, Body, HTTPException, status

from smartkitchien_api.models.user import User, UserPublic, user_example
from smartkitchien_api.security.security import get_password_hash

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserPublic)
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
                detail='O nome de usuário já existe',
            )
        elif username_exist.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='O e-mail já existe',
            )

    user.password = get_password_hash(user.password)

    await user.insert()

    return UserPublic(**user.model_dump())

from beanie.operators import Or
from fastapi import APIRouter, Body, HTTPException, status

from smartkitchen_api.messages.users import InformationUsers
from smartkitchen_api.models.user import User, user_example
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    DefaultAnswer,
    TypeAnswers,
)
from smartkitchen_api.security.security import get_password_hash

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=DefaultAnswer,
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
            detail = AnswerDetail(
                status=status.HTTP_409_CONFLICT,
                type=TypeAnswers.CONFLICT,
                title=InformationUsers.USERNAME_ALREADY_EXISTS['title'],
                msg=InformationUsers.USERNAME_ALREADY_EXISTS['msg'],
                loc=InformationUsers.USERNAME_ALREADY_EXISTS['loc'],
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail.model_dump(),
            )
        elif username_exist.email == user.email:
            detail = AnswerDetail(
                status=status.HTTP_409_CONFLICT,
                type=TypeAnswers.CONFLICT,
                title=InformationUsers.EMAIL_ALREADY_EXISTS['title'],
                msg=InformationUsers.EMAIL_ALREADY_EXISTS['msg'],
                loc=InformationUsers.EMAIL_ALREADY_EXISTS['loc'],
            )
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail.model_dump(),
            )

    user.password = get_password_hash(user.password)

    await user.insert()

    detail = AnswerDetail(
        status=status.HTTP_201_CREATED,
        type=TypeAnswers.SUCCESS,
        title=InformationUsers.USER_CREATED['title'],
        msg=InformationUsers.USER_CREATED['msg'],
    )

    return DefaultAnswer(detail=detail)

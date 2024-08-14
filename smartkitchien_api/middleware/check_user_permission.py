from beanie import PydanticObjectId
from fastapi import HTTPException, status

from smartkitchien_api.messages.generic import InformationGeneric
from smartkitchien_api.schema.standard_answer import (
    AnswerDetail,
    TypeAnswers,
)


def check_user_permission(
    current_user_id: PydanticObjectId | None, user_id: PydanticObjectId
):
    detail = AnswerDetail(
        status=status.HTTP_400_BAD_REQUEST,
        type=TypeAnswers.BAD_REQUEST,
        title=InformationGeneric.ID_MISMATCH['title'],
        msg=InformationGeneric.ID_MISMATCH['msg'],
        loc=InformationGeneric.ID_MISMATCH['loc'],
    )

    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail.model_dump(),
        )

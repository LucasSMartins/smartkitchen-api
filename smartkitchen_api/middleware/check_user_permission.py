from beanie import PydanticObjectId
from fastapi import HTTPException, status

from smartkitchen_api.messages.generic import InformationGeneric
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    TypeAnswers,
)


def check_user_permission(
    current_user_id: PydanticObjectId | None, user_id: PydanticObjectId
):
    detail_error = [
        AnswerDetail(
            status=status.HTTP_400_BAD_REQUEST,
            type=TypeAnswers.BAD_REQUEST,
            title=InformationGeneric.ID_MISMATCH['title'],
            msg=InformationGeneric.ID_MISMATCH['msg'],
            loc=InformationGeneric.ID_MISMATCH['loc'],
        ).model_dump()
    ]

    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_error
        )

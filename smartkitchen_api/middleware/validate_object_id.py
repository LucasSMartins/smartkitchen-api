from typing import Annotated

from bson import ObjectId
from fastapi import HTTPException, Path, status

from smartkitchen_api.messages.users import InformationUsers
from smartkitchen_api.schema.standard_answer import (
    AnswerDetail,
    TypeAnswers,
)

"""
    TODO: O regex que tem no Path() impede que eu mande
    uma string que não seja
    do padrão do ObjectId mas eu criei um middleware só para validar,
    oque faz sentido aqui ??
"""


def validate_object_id(
    user_id: Annotated[
        str,
        Path(
            title='The ID of the item to get',
            description='The unique identifier for the item',
            regex=r'^[a-fA-F0-9]{24}$',
        ),
    ],
):
    if not ObjectId.is_valid(user_id):
        detail_error = [
            AnswerDetail(
                status=status.HTTP_400_BAD_REQUEST,
                type=TypeAnswers.BAD_REQUEST,
                title=InformationUsers.INVALID_USER_ID['title'],
                msg=InformationUsers.INVALID_USER_ID['msg'],
                loc=InformationUsers.INVALID_USER_ID['loc'],
            ).model_dump()
        ]

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail_error
        )

    return user_id

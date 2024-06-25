from typing import Annotated

from bson import ObjectId
from fastapi import HTTPException, Path, status

from smartkitchen_api.api.schema.default_answer import DefaultAnswer, StatusMsg

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=DefaultAnswer(
                status=StatusMsg.FAIL, msg='Invalid user ID'
            ).model_dump(),
        )
    return user_id

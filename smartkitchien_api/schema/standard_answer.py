from typing import Any

from pydantic import BaseModel, Field


class TypeAnswers(BaseModel):
    SUCCESS: str = 'success'
    BAD_REQUEST: str = 'bad_request'
    NOT_FOUND: str = 'not_found'
    INTERNAL_SERVER_ERROR: str = 'internal_server_error'
    CONFLICT: str = 'conflict'
    UNAUTHORIZED: str = 'unauthorized'
    FORBIDDEN: str = 'forbidden'
    PAYMENT_REQUIRED: str = 'payment_required'
    TOO_MANY_REQUESTS: str = 'too_many_requests'
    REQUEST_TIMEOUT: str = 'request_timeout'


class AnswerDetail(BaseModel):
    type: str = Field(...)
    title: str = Field(...)
    status: int = Field(...)
    msg: str = Field(...)
    loc: list[str] | None = None
    instance: str | None = None
    data: Any | None = None
    """
        Exemplo de como deve ser a resposta da api
        deve ser usado entre 400 e 500
        {
            "type": "error_validation",
            "title": "Erro de validação",
            "status": 400,
            "loc": ['path|body|etc...', 'user_id|etc...'],
            "msg": Um ou mais campos do formulário estão inválidos"
            },
            "instance": "/usuarios/novo"
        }
    """


class DefaultAnswer(BaseModel):
    detail: AnswerDetail

from pydantic import BaseModel, Field

"""
    {
        "type": "error_validation",
        "title": "Erro de validação",
        "status": 400,
        "detail": "Um ou mais campos do formulário estão inválidos.",
        "instance": "/usuarios/novo"
    }
"""


class ValidationError(BaseModel):
    type: str = Field(...)
    title: str = Field(...)
    status: int = Field(...)
    detail: str = Field(...)
    instance: str | None = None


class TypesErrorEmail(BaseModel):
    REQUIRED_FIELD_EMAIL: str = 'O campo email está faltando.'

    EMAIL_WITHOUT_AT_SIGN: str = 'O email esta sem o, @ arroba.'
    EMAIL_WITHOUT_DOMAIN: str = 'O email esta sem o domínio.'
    EMAIL_WITHOUT_EXTENSION: str = 'O email esta sem a extensão.'
    EMAIL_WITHOUT_CHARACTERS: str = 'O email esta sem vazio.'

    EMAIL_WITH_MULTIPLE_AT_SIGN: str = 'O email está com multiplos @ arrobas.'
    EMAIL_WITH_INVALID_CHARACTER: str = 'O email está com caracters inválidos'
    EMAIL_WITH_SPACE: str = 'O email não pode conter espaços'
    EMAIL_WITH_INVALID_DOMAIN: str = 'O email está com o dominio inválido.'
    EMAIL_WITH_NON_ALLOWED_CHARACTER: str = 'O email contém caracteres não permitidos'

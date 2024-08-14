from pydantic import BaseModel


class InformationGeneric(BaseModel):
    ID_MISMATCH: dict = {
        'title': 'ID Mismatch',
        'msg': 'The provided ID does not match the expected value.',
        'loc': ['path', 'user_id'],
    }

    INTERNAL_SERVER_ERROR: dict = {
        'title': 'Internal Server Error',
        'msg': 'An unexpected error occurred on the server.',
        'loc': ['internal', 'server'],
    }

    INVALID_CREDENTIALS: dict = {
        'title': 'Invalid Credentials',
        'msg': 'The username or password provided is incorrect.',
    }

    UNAUTHORIZED: dict = {
        'title': 'Unauthorized',
        'msg': 'You are not authorized to perform this action.',
        'loc': ['', ''],
    }

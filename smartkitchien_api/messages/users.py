from pydantic import BaseModel


class InformationUsers(BaseModel):
    USER_DELETED: dict = {
        'title': 'User Deleted',
        'msg': 'The user was successfully deleted.',
    }

    USER_FOUND: dict = {
        'title': 'User Found',
        'msg': 'The user was successfully found.',
    }

    USER_UPDATED: dict = {
        'title': 'User Updated',
        'msg': 'The user information was successfully updated.',
    }

    USER_CREATED: dict = {
        'title': 'User Created',
        'msg': 'The user account was successfully created.',
    }

    EMAIL_ALREADY_EXISTS: dict = {
        'title': 'Email Already Exists',
        'msg': 'A user with this email address already exists.',
        'loc': ['body', 'email'],
    }

    USERNAME_ALREADY_EXISTS: dict = {
        'title': 'Username Already Exists',
        'msg': 'A user with this username already exists.',
        'loc': ['body', 'username'],
    }

    USER_NOT_FOUND: dict = {
        'title': 'User Not Found',
        'msg': 'The specified user could not be found in the system.',
        'loc': ['path', 'user_id'],
    }

    USER_ALREADY_EXISTS: dict = {
        'title': 'User Already Exists',
        'msg': 'A user with the same username or email already exists in the system.',
        'loc': ['body', 'username'],
    }

    INVALID_USER_ID: dict = {
        'title': 'Invalid User ID',
        'msg': 'The provided user ID is not valid.',
        'loc': ['path', 'user_id'],
    }

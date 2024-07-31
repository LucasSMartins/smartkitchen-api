from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from smartkitchien_api.config.settings import setting
from smartkitchien_api.models.user import User

# https://polar.sh/frankie567/posts/introducing-pwdlib-a-modern-password-hash-helper-for-python

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token/')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(payload_data: dict, expires_delta: timedelta | None = None):
    to_encode = payload_data.copy()

    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])

        username: str = payload.get('sub')

        if not username:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await User.find(User.username == username).first_or_none()

    if not user:
        raise credentials_exception

    return user

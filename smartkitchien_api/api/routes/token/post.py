from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from smartkitchien_api.models.user import User
from smartkitchien_api.schema.token import Token
from smartkitchien_api.security.security import create_access_token, verify_password

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=Token)
async def login_for_acess_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Aqui eu defino se o Login será por e-mail ou por username
    user = await User.find(User.username == form_data.username).first_or_none()

    # if not user or not verify_password(form_data.password, user.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail='O email ou senha estão incorretos',
    #         headers={'WWW-Authenticate': 'Bearer'},
    #     )

    access_token = create_access_token(payload_data={'sub': user.username})

    return Token(access_token=access_token, token_type='bearer')

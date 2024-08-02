from fastapi import APIRouter

# from smartkitchien_api.api.endpoints.pantry.post import router as pantry_delete
# from smartkitchien_api.api.endpoints.pantry.post import router as pantry_get
from smartkitchien_api.api.endpoints.pantry.post import router as pantry_post

# from smartkitchien_api.api.endpoints.pantry.post import router as pantry_put
from smartkitchien_api.api.endpoints.token.post import router as token_post
from smartkitchien_api.api.endpoints.users.delete import router as user_delete
from smartkitchien_api.api.endpoints.users.get import router as users_get
from smartkitchien_api.api.endpoints.users.post import router as user_post
from smartkitchien_api.api.endpoints.users.put import router as user_put

api_router = APIRouter()

api_router.include_router(user_delete, prefix='/users', tags=['Users'])
api_router.include_router(users_get, prefix='/users', tags=['Users'])
api_router.include_router(user_post, prefix='/users', tags=['Users'])
api_router.include_router(user_put, prefix='/users', tags=['Users'])

api_router.include_router(pantry_post, prefix='/pantry', tags=['Pantry'])
# api_router.include_router(pantry_delete, prefix='/pantry', tags=['Pantry'])
# api_router.include_router(pantry_get, prefix='/pantry', tags=['Pantry'])
# api_router.include_router(pantry_put, prefix='/pantry', tags=['Pantry'])


api_router.include_router(token_post, prefix='/token', tags=['Token'])

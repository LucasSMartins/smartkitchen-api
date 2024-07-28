from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from smartkitchien_api.config.settings import setting
from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.models.user import User


async def init_db():
    client = AsyncIOMotorClient(setting.DATABASE_URL)

    await init_beanie(database=client.smartkitchien, document_models=[User, Pantry])

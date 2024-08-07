# import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from smartkitchien_api.config.settings import setting
from smartkitchien_api.models.cookbook import Cookbook
from smartkitchien_api.models.pantry import Pantry
from smartkitchien_api.models.shopping_cart import ShoppingCart
from smartkitchien_api.models.user import User

# logging.basicConfig(level=logging.INFO)


async def init_db():
    try:
        client = AsyncIOMotorClient(setting.DATABASE_URI)
        await client.admin.command('ping')  # Verifica se a conexão está ativa
        await init_beanie(
            database=client.smartkitchien,
            document_models=[User, Pantry, ShoppingCart, Cookbook],
        )
    except Exception as e:
        print(e)
        # logging.error(f'Erro ao inicializar o banco de dados: {e}')

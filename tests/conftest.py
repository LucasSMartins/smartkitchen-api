import pytest
from beanie import init_beanie
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from smartkitchien_api.main import app
from smartkitchien_api.models.user import User


@pytest.fixture()
async def setup_db():
    # Setup the MongoDB client and database
    client = AsyncIOMotorClient('mongomock://localhost')

    database = client.test_db

    # Initialize Beanie with the database and models
    await init_beanie(database, document_models=[User])

    yield database

    client.close()


@pytest.fixture()
def client(setup_db):
    # Use TestClient for synchronous testing, without async context manager
    with TestClient(app) as client:
        yield client

    # Clear any dependency overrides if used
    app.dependency_overrides.clear()

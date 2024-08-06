import pytest
from fastapi import status
from fastapi.testclient import TestClient

from smartkitchien_api.main import app

# Crie um cliente de teste para a aplicação FastAPI
client = TestClient(app)


@pytest.mark.asyncio()
async def get_token():
    response = client.post(
        '/api/token',
        form_data={
            'username': 'usertest',
            'password': 'myS&cret007',
        },
    )

    assert response.status_code == status.HTTP_200_OK

from datetime import datetime

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio()
async def test_create_user(client: TestClient):
    response = client.post(
        '/api/users',
        json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'Secure!Pass1',
        },
    )

    if response.status_code != status.HTTP_201_CREATED:
        pytest.fail(
            f"""Expected status code {status.HTTP_201_CREATED}, but got
            {response.status_code}"""
        )

    response_data = response.json()

    if response_data['username'] != 'testuser':
        pytest.fail(
            f"Expected username 'testuser', but got {response_data['username']}"
        )

    if response_data['email'] != 'testuser@example.com':
        pytest.fail(
            f"Expected email 'testuser@example.com', but got {response_data['email']}"
        )

    if 'password' in response_data:
        pytest.fail('Password should not be in the response')

    created_at = response_data.get('created_at', None)
    if not created_at:
        pytest.fail("Missing 'created_at' field in response")

    try:
        datetime.strptime(created_at, '%d/%m/%Y %H:%M:%S')
    except ValueError:
        pytest.fail(f"Invalid date format for 'created_at': {created_at}")

    expected_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'created_at': created_at,
    }

    if response_data != expected_data:
        pytest.fail(
            f"""Response data does not match expected data. Expected:
            {expected_data}, but got: {response_data}"""
        )

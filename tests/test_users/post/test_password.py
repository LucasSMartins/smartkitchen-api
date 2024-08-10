import pytest
from fastapi import status


@pytest.mark.asyncio()
async def test_required_field_password(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'missing'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_lt_8(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'my',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'string_too_short'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_character_uppercase(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'mysecret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validatest_password_must_contain_least_one_lowercase_letter(
    client,
):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'MYS&CRET007',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_special_character(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'mySecret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']


@pytest.mark.asyncio()
async def test_password_validation_must_contain_number(client):
    new_user = {
        'username': 'usertest',
        'email': 'usertest@example.com',
        'password': 'myS&cret',
    }

    response = client.post('/api/users', json=new_user)

    msg = response.json()['detail'][0]  # type: ignore

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert msg['type'] == 'value_error'
    assert msg['loc'] == ['body', 'password']

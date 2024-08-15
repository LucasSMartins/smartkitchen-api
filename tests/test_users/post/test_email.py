import pytest
from fastapi import status


@pytest.mark.asyncio()
async def test_email_exist(client):
    new_user = {
        'username': 'testuser_email',
        'email': 'testuser@example.com',
        'password': 'myS&cret007',
    }

    # Crie um usuário existente
    await User(
        username='testuser', email='testuser@example.com', password='myS&cret007'
    ).create()

    # Faça uma requisição POST para a rota de criação de usuário
    response = client.post('/api/users', json=new_user)

    # Verifique se a requisição foi bem-sucedida
    assert response.status_code == status.HTTP_409_CONFLICT
  


@pytest.mark.asyncio()
async def test_required_field_email(client):
    new_user = {
        'username': 'testuser',
        'password': 'myS&cret007',
    }
    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



@pytest.mark.asyncio()
async def test_email_validation_without_at_sign(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuserexample.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_email_validation_with_space(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser @example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



@pytest.mark.asyncio()
async def test_email_validation_with_invalid_character(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example!.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_email_validation_without_domain(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_email_validation_with_invalid_domain(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.invalid',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_email_validation_with_multiple_at(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com@example.com',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_email_validation_with_non_allowed_character(client):
    new_user = {
        'username': 'testuser',
        'email': 'testuser@example.com£',
        'password': 'myS&cret007',
    }

    response = client.post('/api/users', json=new_user)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

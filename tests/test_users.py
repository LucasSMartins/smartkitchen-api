from http import HTTPStatus


def test_read_users_OK(client):
    response = client.get('/api/users/')
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data['status'] == 'success'
    assert data['msg'] == 'Users found'
    assert isinstance(data['data'], list)

    if data['data']:
        for user in data['data']:
            assert 'username' in user
            assert 'email' in user


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=- GET by user_id -=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'joao',
            'email': 'joaozinho123@example.com',
            'password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'username': 'joao',
        'email': 'joaozinho123@example.com',
    }


def test_visualize_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {
        'users': [
            {
                'username': 'joao',
                'email': 'joaozinho123@example.com',
            }
        ]
    }


def test_user_update(client):
    # I always try to pass a model to this route, so we can get smth out of it
    response = client.put(
        '/users/1',
        json={
            'username': 'joao',
            'email': 'joaozinho123@example.com',
            'password': '12345',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
            'username': 'joao',
            'email': 'joaozinho123@example.com'
    }


def test_user_delete(client):
    response = client.delete('users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}

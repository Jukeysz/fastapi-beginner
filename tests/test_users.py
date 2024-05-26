from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_username_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'dasf@dsad.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_email_already_registered(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Testes',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


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

    assert response.json() == {'users': []}


def test_visualize_users_with_users(client, user):
    response = client.get('/users/')
    # be careful while validating pydantic models with sqlalchemy models
    # I need to configure the schemas accordingly
    user_schema = UserPublic.model_validate(user).model_dump()

    assert response.json() == {'users': [user_schema]}


def test_user_delete(client, user, token):
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_user_update(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
    }

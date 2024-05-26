from http import HTTPStatus


def test_get_token(client, user):
    # here I need to use the monkey patching in order to make it work
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token

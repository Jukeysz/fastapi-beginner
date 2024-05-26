from http import HTTPStatus

import pytest
from fastapi import HTTPException
from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']


@pytest.mark.asyncio()
async def test_security_user_credentials_exception(session, invalid_token):
    with pytest.raises(HTTPException) as tst:
        await get_current_user(session=session, token=invalid_token)
    assert tst.value.status_code == HTTPStatus.UNAUTHORIZED

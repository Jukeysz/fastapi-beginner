from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
            username='joao',
            password='12345',
            email='joaozinho123@example.com',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'joao'))

    assert user.username == 'joao'


# We create a new row in the table and commit it. Thus, we are able to make
# a query and assertions about it

from sqlalchemy import select

from fast_zero.models import Todo, User


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


def test_create_user_task(session, user):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos

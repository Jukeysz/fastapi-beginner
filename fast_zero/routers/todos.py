from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Todo, User
from fast_zero.schemas import (
    Message,
    TodoList,
    TodoPublic,
    TodoSchema,
    TodoUpdate,
)
from fast_zero.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
Sessions = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TodoPublic)
def create_new_task(
    session: Sessions,
    user: CurrentUser,
    todo: TodoSchema,
):
    user_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id
    )

    session.add(user_todo)
    session.commit()
    session.refresh(user_todo)

    return user_todo


@router.get('/', response_model=TodoList)
def visualize_tasks( # noqa
    session: Sessions,
    user: CurrentUser,
    title: str = Query(None),
    description: str = Query(None),
    state: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))

    if description:
        query = query.filter(Todo.description.contains(description))

    if state:
        query = query.filter(Todo.state == state)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.patch('/{task_id}', response_model=TodoPublic)
def update_todo(
    task_id: int,
    user: CurrentUser,
    session: Sessions,
    todo_info: TodoUpdate,
):
    todo_db = session.scalar(
        select(Todo).where(
            and_(Todo.user_id == user.id, Todo.id == task_id)
        )
    )
    if not todo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Invalid todo identifier',
        )

    # items() returns a list of tuples, those tuples contain key-value
    # pairs, so we can take those values concisely

    # setattr will only replace the keys that are matched with the
    # 'for key' placeholder
    for key, value in todo_info.model_dump(exclude_unset=True).items():
        setattr(todo_db, key, value)

    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)

    return todo_db


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(
    todo_id: int,
    user: CurrentUser,
    session: Sessions,
):
    todo_db = session.scalar(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user.id)
    )

    if not todo_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Invalid todo identifier',
        )

    session.delete(todo_db)
    session.commit()

    return {'message': 'Task deleted'}

from fastapi import APIRouter, Depends, Response
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from models.User import User
from schemes.Task import (
    TaskCreate, 
    TaskReadDetail,
    TaskReadList,
    TaskCreatedReponse
)
from sqlalchemy import (
    select,
    insert,
    join,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession
from models.Task import Task


router_tasks= APIRouter(prefix="/tasks")


@router_tasks.get("/", response_model=TaskReadList)
async def api_get_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(Task)
    result = await session.execute(query)
    tasks = result.scalars().all()
    return TaskReadList(tasks=tasks)


@router_tasks.get("/{task_id}", response_model=TaskReadDetail)
async def api_get_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Task, User).select_from(join(Task, User, Task.user_id == User.id)).where(Task.id == task_id)
    result = await session.execute(query)
    task, user = result.fetchone()
    return TaskReadDetail(**task.__dict__, user=user)


@router_tasks.post("/", response_model=TaskCreatedReponse)
async def api_create_task(task_create_form: TaskCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(Task).values(
        description=task_create_form.description,
        user_id=task_create_form.user_id
    ).returning(Task.id)
    result = await session.execute(query)
    await session.commit()
    task_id = result.scalar()
    return TaskCreatedReponse(id=task_id)


@router_tasks.delete("/{task_id}", response_model=TaskReadDetail)
async def api_delete_task(task_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(Task).where(Task.id == task_id)
    await session.execute(query)
    await session.commit()
    return Response(status_code=200)
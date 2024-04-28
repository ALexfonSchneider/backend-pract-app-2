from hashlib import sha256
from fastapi import APIRouter, HTTPException, Depends, Response
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from schemes.User import (
    UserCreate,
    UserCreatedReponse,
    UserPatch,
    UserRead,
    UserReadList, 
    UserUpdate
)
from sqlalchemy import (
    select,
    insert,
    update,
    delete,
)
from sqlalchemy.ext.asyncio import AsyncSession
from models.User import User
from schemes.User import UserCreate


def hash_password(password: str):
    return sha256(password.encode()).hexdigest()


router_users = APIRouter(prefix="/users")


@router_users.get("/", response_model=UserReadList)
async def api_get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return UserReadList(users=[UserRead(id=user.id, first_name=user.first_name, last_name=user.last_name, email=user.email, join_date=user.join_date) for user in users])


@router_users.get("/{user_id}", response_model=UserRead, responses={"404": {"detail": "user does not exist"}})
async def api_get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="user does not exist")
    return user


@router_users.post("/", response_model=UserCreatedReponse)
async def api_create_user(user_create_form: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = insert(User).values(
        first_name= user_create_form.first_name,
        last_name=user_create_form.last_name,
        email=user_create_form.email,
        password_hash=hash_password(user_create_form.password)
    ).returning(User.id)
    result = await session.execute(query)
    user_id = result.scalar()
    await session.commit()
    return UserCreatedReponse(id=user_id)


@router_users.put("/{user_id}", responses={"404": {"detail": "user does not exist"}})
async def api_update_user(user_id: int, user: UserUpdate, session: AsyncSession = Depends(get_async_session)):
    query = update(User).where(User.id == user_id).values(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
    await session.execute(query)
    await session.commit()
    return Response(status_code=201)


@router_users.patch("/")
async def api_patch_user(user_id: int, user: UserPatch, session: AsyncSession = Depends(get_async_session)):
    query = update(User).where(User.id == user_id).values(
        **user.dict(exclude_unset=True)
    )
    await session.execute(query)
    await session.commit()
    return Response(status_code=201)


@router_users.delete("/{user_id}", responses={"404": {"detail": "user does not exist"}})
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(User).where(User.id == user_id)
    await session.execute(query)
    await session.commit()
    return Response(status_code=200)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, check_password, create_access_token
from app.db import schemas, models
from app.db.database import get_db

auth_router = APIRouter(prefix= "/auth" , tags=["Auth"])


@auth_router.post("/register", summary="регистрация нового пользователя")
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user_db = await db.execute(
        select(models.User).filter(user.username == models.User.username))  # проверка пользователя по никнейму
    user_db = user_db.scalars().first()  # получения данных пользователя
    if user_db:
        raise HTTPException(status_code=400, detail="такой пользователь уже существует")
    password_hash = get_password_hash(user.password)
    new_user = models.User(username=user.username, password=password_hash)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@auth_router.post("/login", summary="логин")
async def login(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user_db = await db.execute(
        select(models.User).filter(user.username == models.User.username))  # проверка пользователя по никнейму
    user_db = user_db.scalars().first()
    if not user_db or not check_password:
        raise HTTPException(status_code=400, detail="неверный логин или пароль")
    access_token = create_access_token(data={"sub": user.username, "id":user_db.id})
    return {"access_token": access_token, "token_type": "bearer"}

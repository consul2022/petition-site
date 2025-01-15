from turtle import title

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db import schemas, models
from app.db.database import get_db

petitions_router = APIRouter(prefix="/petition", tags=["Petition"])


@petitions_router.post("/", summary="создание петиции")
async def create_petition(petition: schemas.PetitionCreate, user: dict = Depends(decode_access_token),
                          db: AsyncSession = Depends(get_db)):
    new_petition = models.Petition(title=petition.title, description=petition.description,
                                   author_petition_id=user["id"])
    db.add(new_petition)
    await db.commit()
    await db.refresh(new_petition)
    return new_petition


@petitions_router.get("/", summary="получение всех петиций")
async def get_petition(db: AsyncSession = Depends(get_db)):
    petition = await db.execute(select(models.Petition))
    return petition.scalars().all()


@petitions_router.get("/{petition_id}", summary="получение конкретной петиции")
async def get_petition_id(petition_id: int, db: AsyncSession = Depends(get_db)):
    petition = await db.execute(select(models.Petition).filter(models.Petition.id == petition_id))
    return petition.scalars().first()

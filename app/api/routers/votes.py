from fastapi import APIRouter, Depends, HTTPException
from select import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db import models
from app.db.database import get_db

votes_router = APIRouter(prefix="/votes", tags=["Votes"])


@votes_router.post("/{petition_id}", summary="голос за петицию")
async def votes_for_petition(petition_id: int, user: dict = Depends(decode_access_token),
                             db: AsyncSession = Depends(get_db)):
    petition = await db.execute(select(models.Petition).filter(models.Petition.id == petition_id))
    petition = petition.scalars().first()
    if not petition:
        raise HTTPException(status_code=404, detail="петиция не найдена")

    vote = await db.execute(
        select(models.Vote).filter(models.Vote.petition_id == petition_id, models.Vote.user_id == user["id"]))
    vote = vote.scalars().all()
    if vote:
        raise HTTPException(status_code=400, detail="вы уже проголосовали")
    new_vote = models.Vote(user_id=user["id"], petition_id=petition_id)
    db.add(new_vote)
    petition.vote +=1
    await db.commit()
    return {"message": "ваш голос учтён"}




@votes_router.delete("/{petition_id}", summary="отозвать голос за петицию")
async def votes_for_petition(petition_id: int, user: dict = Depends(decode_access_token),
                             db: AsyncSession = Depends(get_db)):
    petition = await db.execute(select(models.Petition).filter(models.Petition.id == petition_id))
    petition = petition.scalars().first()
    if not petition:
        raise HTTPException(status_code=404, detail="петиция не найдена")

    vote = await db.execute(
        select(models.Vote).filter(models.Vote.petition_id == petition_id, models.Vote.user_id == user["id"]))
    vote = vote.scalars().first()
    if not vote:
        raise HTTPException(status_code=400, detail="ваш голос не найден")
    await db.delete(vote)
    petition.vote -=1
    await db.commit()
    return {"message": "ваш голос отозван"}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas import QueueCreate, QueueOut
from deps import get_db_dep, require_roles
import crud

router = APIRouter(prefix="/queues", tags=["queues"])

@router.post("/", response_model=QueueOut, dependencies=[Depends(require_roles("admin"))])
async def create_queue(queue_in: QueueCreate, db: AsyncSession = Depends(get_db_dep)):
    q = await crud.create_queue(db, queue_in.nom, queue_in.institution, queue_in.max_capacity)
    return q

@router.get("/", response_model=List[QueueOut])
async def list_queues(skip: int = 0, limit: int = 50, search: str = None, db: AsyncSession = Depends(get_db_dep)):
    return await crud.list_queues(db, skip=skip, limit=limit, search=search)

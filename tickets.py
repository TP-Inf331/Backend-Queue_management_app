from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas import TicketCreate, TicketOut
from deps import get_db_dep, require_roles, get_current_user
import crud

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=TicketOut)
async def create_ticket(ticket_in: TicketCreate, db: AsyncSession = Depends(get_db_dep), current_user = Depends(get_current_user)):
    user_id = ticket_in.user_id or current_user.user_id
    ticket = await crud.create_ticket(db, queue_id=ticket_in.queue_id, user_id=user_id, prioritaire=ticket_in.prioritaire)
    return ticket

@router.post("/{queue_id}/next", response_model=TicketOut, dependencies=[Depends(require_roles("agent","admin"))])
async def call_next(queue_id: int, db: AsyncSession = Depends(get_db_dep)):
    ticket = await crud.call_next(db, queue_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="No waiting tickets")
    return ticket

@router.post("/{ticket_id}/cancel", response_model=TicketOut)
async def cancel_ticket(ticket_id: int, db: AsyncSession = Depends(get_db_dep), current_user = Depends(get_current_user)):
    ticket = await crud.get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    # allow owner or admin/agent to cancel
    if ticket.user_id != current_user.user_id and current_user.role not in ("admin","agent"):
        raise HTTPException(status_code=403, detail="Forbidden")
    return await crud.cancel_ticket(db, ticket_id)

@router.get("/history", response_model=List[TicketOut])
async def ticket_history(skip: int = 0, limit: int = 50, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db_dep)):
    return await crud.ticket_history(db, user_id=current_user.user_id, skip=skip, limit=limit)

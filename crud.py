from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, or_
from models import User, Queue, Ticket, Notification
from security import get_password_hash
from typing import Optional, List
import secrets
from fastapi import HTTPException

# Users
async def create_user(db: AsyncSession, nom: str, email: str, password: str, role: str = "client", phone: Optional[str] = None) -> User:
    hashed = get_password_hash(password)
    user = User(nom=nom, email=email, mot_de_passe_hash=hashed, role=role, phone=phone)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    q = await db.execute(select(User).where(User.email == email))
    return q.scalars().first()

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    q = await db.execute(select(User).where(User.user_id == user_id))
    return q.scalars().first()

async def list_users(db: AsyncSession, skip: int = 0, limit: int = 100, search: Optional[str]=None) -> List[User]:
    stmt = select(User)
    if search:
        stmt = stmt.where(or_(User.nom.ilike(f'%{search}%'), User.email.ilike(f'%{search}%')))
    stmt = stmt.offset(skip).limit(limit)
    q = await db.execute(stmt)
    return q.scalars().all()

# Queues
async def create_queue(db: AsyncSession, nom: str, institution: Optional[str], max_capacity: Optional[int]) -> Queue:
    code_unique = secrets.token_hex(8)
    queue = Queue(nom=nom, institution=institution, code_unique=code_unique, max_capacity=max_capacity)
    db.add(queue)
    await db.commit()
    await db.refresh(queue)
    return queue

async def get_queue(db: AsyncSession, queue_id: int) -> Optional[Queue]:
    q = await db.execute(select(Queue).where(Queue.queue_id == queue_id))
    return q.scalars().first()

async def list_queues(db: AsyncSession, skip: int = 0, limit: int = 100, search: Optional[str]=None):
    stmt = select(Queue)
    if search:
        stmt = stmt.where(Queue.nom.ilike(f'%{search}%') | Queue.institution.ilike(f'%{search}%'))
    stmt = stmt.offset(skip).limit(limit)
    q = await db.execute(stmt)
    return q.scalars().all()

# Tickets
async def next_ticket_number(db: AsyncSession, queue_id: int) -> int:
    q = await db.execute(select(func.max(Ticket.numero)).where(Ticket.queue_id == queue_id))
    max_num = q.scalar_one_or_none()
    return (max_num or 0) + 1

async def create_ticket(db: AsyncSession, queue_id: int, user_id: Optional[int], prioritaire: bool=False) -> Ticket:
    numero = await next_ticket_number(db, queue_id)
    ticket = Ticket(queue_id=queue_id, user_id=user_id, numero=numero, statut="attente", prioritaire=prioritaire)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def get_ticket(db: AsyncSession, ticket_id: int) -> Optional[Ticket]:
    q = await db.execute(select(Ticket).where(Ticket.ticket_id == ticket_id))
    return q.scalars().first()

async def cancel_ticket(db: AsyncSession, ticket_id: int) -> Ticket:
    ticket = await get_ticket(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.cancelled = True
    ticket.statut = "annule"
    await db.commit()
    await db.refresh(ticket)
    return ticket

async def call_next(db: AsyncSession, queue_id: int) -> Optional[Ticket]:
    q = await db.execute(
        select(Ticket)
        .where(Ticket.queue_id==queue_id, Ticket.statut=="attente", Ticket.cancelled==False)
        .order_by(desc(Ticket.prioritaire), Ticket.heure_arrivee)
    )
    next_ticket = q.scalars().first()
    if not next_ticket:
        return None
    next_ticket.statut = "appele"
    await db.commit()
    await db.refresh(next_ticket)
    return next_ticket

async def ticket_history(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    q = await db.execute(
        select(Ticket)
        .where(Ticket.user_id==user_id)
        .order_by(Ticket.heure_arrivee.desc())
        .offset(skip)
        .limit(limit)
    )
    return q.scalars().all()

# Notifications
async def create_notification(db: AsyncSession, user_id: int, type_: str, message: str) -> Notification:
    n = Notification(user_id=user_id, type=type_, message=message)
    db.add(n)
    await db.commit()
    await db.refresh(n)
    return n

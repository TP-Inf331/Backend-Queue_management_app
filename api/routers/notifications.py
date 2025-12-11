from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import NotificationCreate, NotificationOut
from app.api.deps import get_db_dep, require_roles
from app.crud import crud
from app.services.notifications import send_notification_async

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationOut, dependencies=[Depends(require_roles("admin","agent"))])
async def create_notification(n_in: NotificationCreate, db: AsyncSession = Depends(get_db_dep)):
    n = await crud.create_notification(db, n_in.user_id, n_in.type, n_in.message)
    await send_notification_async(n_in.user_id, n_in.type, n_in.message)
    return n

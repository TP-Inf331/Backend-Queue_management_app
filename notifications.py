from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import NotificationCreate, NotificationOut
from deps import get_db_dep, require_roles
import crud
from notifications_utils import send_notification_async  # <-- import from new file

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationOut, dependencies=[Depends(require_roles("admin","agent"))])
async def create_notification(n_in: NotificationCreate, db: AsyncSession = Depends(get_db_dep)):
    n = await crud.create_notification(db, n_in.user_id, n_in.type, n_in.message)
    await send_notification_async(n_in.user_id, n_in.type, n_in.message)
    return n

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.api.deps import get_db_dep, require_roles, get_current_user
from app.schemas.schemas import UserCreate, UserOut
from app.crud import crud

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOut, dependencies=[Depends(require_roles("admin"))])
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db_dep)):
    existing = await crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = await crud.create_user(db, nom=user_in.nom, email=user_in.email, password=user_in.mot_de_passe, role=user_in.role)
    return user

@router.get("/", response_model=List[UserOut], dependencies=[Depends(require_roles("admin"))])
async def list_users(skip: int = 0, limit: int = 50, search: str = None, db: AsyncSession = Depends(get_db_dep)):
    return await crud.list_users(db, skip=skip, limit=limit, search=search)

@router.get("/me", response_model=UserOut)
async def read_own_user(current_user = Depends(get_current_user)):
    return current_user

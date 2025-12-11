from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.api.deps import get_db_dep
from app.crud import crud
from app.schemas.schemas import Token
from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db_dep)):
    user = await crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form_data.password, user.mot_de_passe_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token_data = {"user_id": user.user_id, "role": user.role}
    access_token = create_access_token(data=token_data, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

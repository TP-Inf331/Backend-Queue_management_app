# app/deps.py
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db  # make sure you have this
from models import User
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db_dep() -> AsyncSession:
    async with get_db() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_dep)):
    # logic to decode token and get the user from db
    user = ...  # retrieve user
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

def require_roles(*roles):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper

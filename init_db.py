import asyncio

from base import Base
from database import engine
import models # Ensure models are registered with Base


async def init() -> None:
    """
    Create all database tables based on the SQLAlchemy models.

    Uses the DATABASE_URL from config/settings (env variable override on Vercel/locally).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed Admin User
    from database import AsyncSessionLocal
    import crud
    
    async with AsyncSessionLocal() as session:
        admin_email = "admin@admin.com"
        admin = await crud.get_user_by_email(session, admin_email)
        if not admin:
            print(f"Creating default admin user: {admin_email}")
            await crud.create_user(
                session, 
                nom="Super Admin", 
                email=admin_email, 
                password="adminpassword", 
                role="admin"
            )
        else:
            print(f"Admin user {admin_email} already exists.")


if __name__ == "__main__":
    asyncio.run(init())




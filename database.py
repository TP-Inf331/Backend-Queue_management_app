from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import config

# Use settings from config.py
settings = config.settings

# Create the async engine
engine = create_async_engine(str(settings.DATABASE_URL), future=True, echo=False)

# Create a session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for getting DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

from pydantic_settings import BaseSettings
from pydantic import AnyUrl
class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = "nalwNlt85XNnrwAx3vi5G4_EqBP_IyN_1UGrsaYBu1o"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "postgresql+asyncpg://queueuser:queue123@localhost:5432/queue_db"
    RATE_LIMIT: int = 60
    class Config:
        env_file = ".env"
settings = Settings()

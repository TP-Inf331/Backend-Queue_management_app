from pydantic import BaseSettings, AnyUrl
class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: AnyUrl
    RATE_LIMIT: int = 60
    class Config:
        env_file = ".env"
settings = Settings()

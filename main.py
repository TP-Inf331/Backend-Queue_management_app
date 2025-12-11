from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import auth, users, queues, tickets, notifications, reports
from app.utils.logger import logger
from app.api.rate_limit import SimpleRateLimitMiddleware

def create_app():
    app = FastAPI(title="Queue Management API", version="1.1")
    app.include_router(auth.router, prefix="/api")
    app.include_router(users.router, prefix="/api")
    app.include_router(queues.router, prefix="/api")
    app.include_router(tickets.router, prefix="/api")
    app.include_router(notifications.router, prefix="/api")
    app.include_router(reports.router, prefix="/api")
    app.add_middleware(SimpleRateLimitMiddleware)
    @app.on_event("startup")
    async def startup():
        logger.info("Starting app")
    return app

app = create_app()

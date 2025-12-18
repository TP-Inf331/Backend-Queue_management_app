from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers from sibling files
from auth import router as auth_router
from users import router as users_router
from queues import router as queues_router
from tickets import router as tickets_router
from notifications import router as notifications_router
from reports import router as reports_router

app = FastAPI(title="Queue Management API")

origins = [
    "http://localhost:4000",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://frontent-queue-management-app.onrender.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(queues_router)
app.include_router(tickets_router)
app.include_router(notifications_router)
app.include_router(reports_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Queue Management API"}

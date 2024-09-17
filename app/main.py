from core.config import settings
from core.security import get_current_user
from db.session import close_db_connection, connect_to_db
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    auth,
    users,
    logs,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código para el evento de inicio
    await connect_to_db()
    yield
    # Código para el evento de cierre
    await close_db_connection()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def version():
    return {"API Versión": "1.0.0"}


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="", tags=["Users"])
app.include_router(logs.router, prefix="", tags=["Logs"], dependencies=[Depends(get_current_user)])


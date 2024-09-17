# app/routes/logs.py
from datetime import datetime
from typing import List

from core.security import get_current_user
from core.utils import get_client_ip
from core.config import settings
from db.session import database as db
from fastapi import APIRouter, Depends, HTTPException, Response
from models.logs import logs
from schemas.logs import LogBase, LogInDB
from sqlalchemy.sql import desc, delete, insert, select

router = APIRouter()

responses = {401: {"description": "Not Autehnticated"}}


# 1. Listar logs
@router.get(
    "/logs",
    response_model=List[LogInDB],
    responses={
        204: {"description": "No se encontraron registros"}
    },
)
async def list_logs():
    query = select(logs).order_by(desc(logs.c.id))
    results = await db.fetch_all(query)
    if not results:
        return Response(status_code=204)
    
    return results


# 2. Crear log
@router.post(
    "/logs",
    response_model=LogInDB,
    responses={
        404: {"description": "Error al crear log"},
        **responses
    },
)
async def create_log(
    log: LogBase,
    current_user: dict = Depends(get_current_user),
    client_ip: str = Depends(get_client_ip)
):
    # solo si el usuario está logueado crea logs
    if not current_user.get("id"):
        raise HTTPException(status_code=401, detail="Usuario no definido")
    user_id_token = current_user.get("id")

    query = (
        insert(logs)
        .values(
            user_id=user_id_token, 
            action=log.action, 
            ip=client_ip,
            created_at=datetime.now(settings.spain_tz)
        )
    )
    log_id = await db.execute(query)

    if not log_id:
        raise HTTPException(status_code=404, detail="Error al crear log")

    query = select(logs).where(logs.c.id == log_id)
    created_log = await db.fetch_one(query)

    return created_log


# 3. Listar logs por usuario
@router.get(
    "/logs/{user_id}",
    response_model=List[LogInDB],
    responses={
        204: {"description": "No se encontraron registros para este usuario"}
    },
)
async def list_logs_by_user(user_id: int):
    query = select(logs).where(logs.c.user_id == user_id).order_by(desc(logs.c.id))
    results = await db.fetch_all(query)
    if not results:
        return Response(status_code=204)
    
    return results


# 4. Eliminar log
@router.delete(
    "/logs/{log_id}",
    response_model=LogInDB,
    responses={**responses},
)
async def delete_log(log_id: int):
    query = delete(logs).where(logs.c.id == log_id)
    result = await db.execute(query)
    if result == 0:
        raise HTTPException(status_code=404, detail="Log no encontrado")
    
    return {"detail": "Log deleted successfully"}

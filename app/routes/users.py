# app/routes/users.py

from typing import List

import bcrypt
from core.security import get_current_user
from databases import Database
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from models.users import users
from schemas.users import UserCreate, UserInDB, UserUpdate
from sqlalchemy.sql import asc, delete, insert, select, update

router = APIRouter()

responses = {404: {"description": "Not found"}}


# 1. Listar usuarios
@router.get(
    "/users",
    response_model=List[UserInDB],
    responses={**responses},
)
async def list_users(
    db: Database = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    # solo si el usuario logueado actual (get_current_user) es staff puede crear usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    query = select(users).order_by(asc(users.c.id))
    results = await db.fetch_all(query)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron usuarios")
    return results


# 1. Listar usuarios ADMIN
@router.get(
    "/users/admin",
    response_model=List[UserInDB],
    responses={
        204: {"description": "No se encontraron usuarios"}
    },
)
async def list_users_admin(
    db: Database = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    # solo si el usuario logueado actual (get_current_user) es staff puede ver usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    query = (
        select(users)
        .where(users.c.is_staff.is_(True))
        .order_by(asc(users.c.id))
    )
    results = await db.fetch_all(query)
    if not results:
        Response(status_code=204)
    return results


# 1. Listar usuarios CLIENT
@router.get(
    "/users/clients",
    response_model=List[UserInDB],
    responses={
        204: {"description": "No se encontraron usuarios"}
    },
)
async def list_users_clients(
    db: Database = Depends(get_db), current_user: dict = Depends(get_current_user)
):
    # solo si el usuario logueado actual (get_current_user) es staff puede ver usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    query = (
        select(users)
        .where(users.c.is_staff.is_(False))
        .order_by(asc(users.c.id))
    )
    results = await db.fetch_all(query)
    if not results:
        return Response(status_code=204)
    
    return results


# 2. Crear usuario
@router.post(
    "/users",
    response_model=UserInDB,
    responses={400: {"detail": "Usuario/email or NIF ya usado."}},
)
async def create_user(
    user: UserCreate,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # solo si el usuario logueado actual (get_current_user) es staff puede crear usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    query = (
        insert(users)
        .values(
            username=user.username,
            email=user.email,
            password=hashed_password,
            name=user.name,
            surname=user.surname,
            phone=user.phone,
            NIF=user.NIF,
            observations=user.observations,
            is_staff=user.is_staff,
        )
    )
    try:
        user_id = await db.execute(query)
        query = select(users).where(users.c.id == user_id)

        return await db.fetch_one(query)
    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e):
            duplicado = str(e).split("Key (")[1].split(")")[0]
            raise HTTPException(
                status_code=400, detail="Datos duplicados: " + duplicado
            )
        else:
            raise HTTPException(status_code=500, detail="Internal server error." + str(e))


# 3. Leer usuario
@router.get("/users/{user_id}", response_model=UserInDB, responses={404: {}})
async def read_user(
    user_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # solo si el usuario logueado actual (get_current_user) es staff puede crear usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    query = select(users).where(users.c.id == user_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


# 4. Actualizar usuario
@router.put("/users/{user_id}", response_model=UserInDB, responses={**responses})
async def update_user(
    user_id: int,
    user: UserUpdate,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # solo si el usuario logueado actual (get_current_user) es staff puede crear usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    if user.password:
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        query = (
            update(users)
            .where(users.c.id == user_id)
            .values(
                username=user.username,
                email=user.email,
                password=hashed_password,
                name=user.name,
                surname=user.surname,
                phone=user.phone,
                NIF=user.NIF,
                observations=user.observations,
                is_staff=user.is_staff,
            )
        )
    else:
        query = (
            update(users)
            .where(users.c.id == user_id)
            .values(
                username=user.username,
                email=user.email,
                name=user.name,
                surname=user.surname,
                phone=user.phone,
                NIF=user.NIF,
                observations=user.observations,
                is_staff=user.is_staff,
            )
        )

    try:
        result = await db.execute(query)
    except Exception as e:
        if "duplicate key value violates unique constraint" in str(e):
            duplicado = str(e).split("Key (")[1].split(")")[0]
            raise HTTPException(
                status_code=400, detail="Datos duplicados: " + duplicado
            )
        else:
            raise HTTPException(
                status_code=500, detail="Internal server error." + str(e)
            )

    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return updated user
    query = select(users).where(users.c.id == user_id)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    
    return result


# 5. Borrar usuario
@router.delete(
        "/users/{user_id}", 
        responses={
            200: {"description": "User deleted successfully", "content": {"application/json": {}}},
            404: {"description": "User not found", "content": {"application/json": {}}},
            401: {"description": "Unauthorized", "content": {"application/json": {}}},
        })
async def delete_user(
    user_id: int,
    db: Database = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    # solo si el usuario logueado actual (get_current_user) es staff puede crear usuarios
    if not current_user.get("is_staff"):
        raise HTTPException(status_code=401, detail="Usuario no autorizado")

    query = delete(users).where(users.c.id == user_id)
    result = await db.execute(query)

    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"detail": "User deleted successfully"}

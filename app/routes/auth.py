# /app/api/auth.py
from datetime import datetime
from typing import Annotated

import bcrypt
import core.security as jwt_utils
from core.config import settings
from core.utils import get_client_ip
from db.session import database as db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.users import users
from models.logs import logs
from schemas.auths import Token

router = APIRouter()


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


@router.post(
    "/token",
    response_model=Token,
    responses={
        400: {"detail": "Incorrect username."},
        401: {"detail": "Incorrect password."},
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    client_ip: str = Depends(get_client_ip)
):
    query = users.select().where(users.c.username == form_data.username)
    user_record = await db.fetch_one(query)

    if not user_record:
        raise HTTPException(status_code=400, detail="Incorrect username.")

    user = dict(user_record)
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password.")

    access_token = jwt_utils.create_access_token(
        data={"sub": form_data.username, "id": user["id"], "is_staff": user["is_staff"]}
    )
    # is token is generate correctly update last_login and add log record
    if access_token is not None:
        query = (
            users.update()
            .where(users.c.id == user["id"])
            .values(last_login=datetime.now(settings.spain_tz))
        )
        await db.execute(query)
        # añado registro al log
        query = (
            logs.insert()
            .values(user_id=user["id"], action="login", ip=client_ip, created_at=datetime.now(settings.spain_tz))
        )
        await db.execute(query)

    return {"access_token": access_token, "token_type": "bearer"}

# app/models/users.py
from db.session import metadata
from sqlalchemy import Boolean, Column, DateTime, Integer, Sequence, String, Table, func

users = Table(
    "users",
    metadata,
    Column("id", Integer, Sequence("users_id_seq"), primary_key=True),
    Column("name", String(50), nullable=False),
    Column("surname", String(50), nullable=False),
    Column("username", String(50), unique=True, index=True, nullable=False),
    Column("email", String(100), unique=True, index=True, nullable=True),
    Column("password", String(100), nullable=False),
    Column("phone", String(20)),
    Column("NIF", String(9), nullable=True),
    Column("observations", String(255), nullable=True),
    Column("is_staff", Boolean, default=False, nullable=False),
    Column("last_login", DateTime(timezone=True), nullable=True, default=None),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)

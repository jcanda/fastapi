# app/models/logs.py
from db.session import metadata
from sqlalchemy import Column, DateTime, Integer, Sequence, String, Table, ForeignKeyConstraint, func

logs = Table(
    "logs",
    metadata,
    Column("id", Integer, Sequence("users_id_seq"), primary_key=True),
    Column("user_id", Integer,nullable=False),
    Column("action", String(255), nullable=False),
    Column("ip", String(150), nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    # foreign key constraint to users table on user_id column 
    ForeignKeyConstraint(
        ['user_id'], 
        ['users.id'], 
        onupdate='CASCADE',
        ondelete='RESTRICT'
    ),
)

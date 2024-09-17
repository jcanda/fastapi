# app/schemas/logs.py

from datetime import datetime
from typing import Optional

from core.config import settings
from pydantic import BaseModel, EmailStr, field_validator


class LogBase(BaseModel):
    action: str

class LogInDB(LogBase):
    id: int
    user_id: int
    ip: str
    created_at: datetime

    # Validators can be added to ensure the data matches specific criteria
    @field_validator("user_id")
    def user_id_must_be_positive(cls, v):
        assert v > 0, "must be a positive integer"
        return v
    
    @field_validator("created_at")
    def convert_utc_to_spain(cls, value: datetime) -> datetime:
        if value is not None:
            return value.astimezone(settings.spain_tz)

    class Config:
        from_attributes = True

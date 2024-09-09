# app/schemas/users.py

from datetime import datetime
from typing import Optional

from core.config import settings
from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    email: Optional[EmailStr]
    phone: Optional[str]
    NIF: Optional[str]
    observations: Optional[str]
    is_staff: bool = False

    # Validators can be added to ensure the data matches specific criteria
    @field_validator("name", "surname")
    def name_must_be_capitalized(cls, v):
        return v.title()

    @field_validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v.lower()

    @field_validator("email")
    def email_is_valid(cls, v):
        assert "@" in v, "must be a valid email"
        return v

    @field_validator("NIF")
    def validate_NIF(cls, v):
        assert len(v) == 9, "NIF should be 9 characters long"
        assert v[-1].isalpha(), "Last character should be a letter"
        return v.upper()


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]

    @field_validator("created_at", "updated_at", "last_login")
    def convert_utc_to_spain(cls, value: datetime) -> datetime:
        if value is not None:
            return value.astimezone(settings.spain_tz)

    class Config:
        from_attributes = True


class UserActive(BaseModel):
    name: str
    surname: str
    username: str
    status: int
    number_exercises: int
    number_exercises_finish: int


class UserActiveInDB(UserActive):
    id: int

    class Config:
        from_attributes = True

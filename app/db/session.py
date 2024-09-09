# app/db/session.py
from core.config import settings
from databases import Database
from sqlalchemy import MetaData

database = Database(settings.DATABASE_URL)
metadata = MetaData()


async def get_db():
    await database.connect()
    try:
        yield database
    finally:
        print("Not Closing connection to database")
        # await database.disconnect()


async def connect_to_db():
    await database.connect()


async def close_db_connection():
    await database.disconnect()

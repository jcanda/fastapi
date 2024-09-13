import os

from pytz import timezone


class Settings:
    PROJECT_NAME: str = "Fastapi API 🔥"
    PROJECT_VERSION: str = "1.0.0"

    # MYSQL CONFIG
    DB_NAME = os.environ.get("MARIADB_DATABASE")
    DB_USER = os.environ.get("MARIADB_USER")
    DB_PASSWORD = os.environ.get("MARIADB_PASSWORD")
    DB_HOST = os.environ.get("MARIADB_HOST")
    DB_PORT = 3306

    DATABASE_URL = f"mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    DATABASE_URL_SYNC = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # CORS CONFIG
    CORS_ALLOWED_ORIGINS = [
        "127.0.0.1",
        "localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]

    # TOKEN CONFIG
    SECRET_KEY = os.getenv(
        "SECRET_KEY", "c!62gdw-sshqfht50%8nzg1y12@#tislm_(&w_kng5no%zi5ua"
    )
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 90

    # Definimos la zona horaria de España
    spain_tz = timezone("Europe/Madrid")


settings = Settings()

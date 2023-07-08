from os import environ, getenv

#from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()


class Settings:
    APP_TITLE = "App Tg"
    ALLOWED_HOST = getenv("ALLOWED_HOST")
    SECRET_KEY = getenv("SECRET_KEY")
    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
    APP_BASE_URL = getenv("APP_BASE_URL")
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM = getenv("ALGORITHM")
    
    TELEBOT_BOT_TOKEN = getenv("TELEBOT_BOT_TOKEN")
    API_ID = getenv("API_ID")
    API_HASH = getenv("API_HASH")
    PHONE = getenv("PHONE")

    DEBUG = bool(getenv("DEBUG"))
    ALLOWED_PORT = int(getenv("PORT"))
    DB_USER = getenv("POSTGRES_USER")
    DB_PASSWORD = environ.get("POSTGRES_PASSWORD")
    DB_DB = environ.get("POSTGRES_DB")
    DB_PORT = environ.get("POSTGRES_PORT")
    DB_HOST = environ.get("POSTGRES_HOST")
    DB_URL = (
        f"sqlite:///./app/database/db/tgtradedb.db"#postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
    )
    TEST_DB = environ.get("POSTGRES_TEST_DB")
    TEST_DB_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB}"
    )
    ACCESS_TOKEN_EXPIRY_TIME = 60 * 30
    REFRESH_TOKEN_EXPIRY_TIME = 60 * 24 * 365
    #PASSWORD_HASHER = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_ALGORITHM = "HS256"
    REDIS_HOST = environ.get("REDIS_HOST", "localhost")
    REDIS_PORT = environ.get("REDIS_PORT", "6379")
    PAGE_SIZE = 50


settings = Settings()


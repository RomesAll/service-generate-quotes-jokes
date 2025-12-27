from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from .logging_conf import logger_setup
import os, logging

load_dotenv()

class ConfigPostgres(BaseSettings):
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    POSTGRES_MODE: str = os.getenv("POSTGRES_MODE")

    @property
    def get_database_url_sync(self):
        return f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

class Config(BaseSettings):
    postgresql: ConfigPostgres = ConfigPostgres()
    logger: logging  = logger_setup.get_logger()

settings = Config()
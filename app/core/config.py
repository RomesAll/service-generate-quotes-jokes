from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from .logging_conf import logger_setup
from pathlib import Path
import os, logging, pika

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

class AuthJWT(BaseSettings):
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    algorithm: str = 'RS256'
    access_token_exp: int = 10

class RedisDB(BaseSettings):
    cache: int = 0

class RedisConfig(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    db: RedisDB = RedisDB()

class CacheConfig(BaseSettings):
    prefix: str = 'fastapi-cache'

class RabbitMQConfig(BaseSettings):
    mq_host: str = 'localhost'
    mq_port: int = 5672
    mq_user: str = 'guest'
    mq_password: str = 'guest'

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
    logger: logging.Logger  = logger_setup.get_logger()
    auth_jwt: AuthJWT = AuthJWT()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()
    rabbitmq: RabbitMQConfig = RabbitMQConfig()

settings = Config()
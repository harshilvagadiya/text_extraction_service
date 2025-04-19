import logging
import os
import pathlib

import loguru
from decouple import Config, RepositoryEnv
from pydantic_settings import BaseSettings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


def load_config():
    env_path = ROOT_DIR / ".env"
    config = Config(RepositoryEnv(env_path))
    env = config("ENVIRONMENT", cast=str).lower()
    env_file = f".env.{env}"
    DOTENV_FILE = os.path.join(ROOT_DIR, env_file)
    config = Config(RepositoryEnv(DOTENV_FILE))
    loguru.logger.info(f"Current Env File | {env_file}")
    return config


config = load_config()


class BackendBaseSettings(BaseSettings): 
    TITLE: str = "Fastapi API" 
    VERSION: str = "0.0.1" 
    TIMEZONE: str = "UTC" 
    DESCRIPTION: str | None = "Default description" 
    DEBUG: bool = config("DEBUG", cast=bool) 
    SERVER_HOST: str = config("BACKEND_SERVER_HOST", default="127.0.0.1", cast=str) 
    SERVER_PORT: int = config("BACKEND_SERVER_PORT", default=8000, cast=int) 
    SERVER_WORKERS: int = config("BACKEND_SERVER_WORKERS", cast=int) 
    API_PREFIX: str = "/api" 
    DOCS_URL: str = "/docs" 
    OPENAPI_URL: str = "/openapi.json" 
    REDOC_URL: str = "/redoc" 
    OPENAPI_PREFIX: str = "" 
    DB_POSTGRES_NAME: str = config("POSTGRES_DB", cast=str) 
    DB_POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", cast=str) 
    DB_POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int) 
    DB_POSTGRES_SCHEMA: str = config("POSTGRES_SCHEMA", cast=str) 
    DB_POSTGRES_USERNAME: str = config("POSTGRES_USERNAME", cast=str) 
    DB_POSTGRES_HOST: str = config("POSTGRES_HOST", cast=str) 
    DB_TIMEOUT: int = config("DB_TIMEOUT", cast=int) 
    DB_POOL_SIZE: int = config("DB_POOL_SIZE", cast=int) 
    DB_MAX_POOL_CON: int = config("DB_MAX_POOL_CON", cast=int) 
    DB_POOL_RECYCLE: int = config("DB_POOL_RECYCLE", cast=int) 
    DB_POOL_OVERFLOW: int = config("DB_POOL_OVERFLOW", cast=int) 
    IS_DB_FORCE_ROLLBACK: bool = config("IS_DB_FORCE_ROLLBACK", cast=bool) 
    IS_DB_EXPIRE_ON_COMMIT: bool = config("IS_DB_EXPIRE_ON_COMMIT", cast=bool) 
    IS_DB_FORCE_ROLLBACK: bool = config("IS_DB_FORCE_ROLLBACK", cast=bool) 
    IS_DB_EXPIRE_ON_COMMIT: bool = config("IS_DB_EXPIRE_ON_COMMIT", cast=bool) 
    API_TOKEN: str = config("API_TOKEN", cast=str) 
    AUTH_TOKEN: str = config("AUTH_TOKEN", cast=str) 
    JWT_TOKEN_PREFIX: str = config("JWT_TOKEN_PREFIX", cast=str) 
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str) 
    JWT_SUBJECT: str = config("JWT_SUBJECT", cast=str) 
    JWT_MIN: int = config("JWT_MIN", cast=int) 
    JWT_HOUR: int = config("JWT_HOUR", cast=int) 
    JWT_DAY: int = config("JWT_DAY", cast=int) 
    REMEMBER_ME_JWT_DAY: int = config("REMEMBER_ME_JWT_DAY", cast=int) 
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY 
    JWT_ACCESS_TOKEN_EXPIRATION_TIME_REMEMBER_ME: int = JWT_MIN * JWT_HOUR * REMEMBER_ME_JWT_DAY 
    IS_ALLOWED_CREDENTIALS: bool = config("IS_ALLOWED_CREDENTIALS", cast=bool) 
    ALLOWED_ORIGINS: list[str] = ["*"] 
    ALLOWED_METHODS: list[str] = ["*"] 
    ALLOWED_HEADERS: list[str] = ["*"] 
    LOGGING_LEVEL: int = logging.INFO 
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access") 
    HASHING_ALGORITHM_LAYER_1: str = config("HASHING_ALGORITHM_LAYER_1", cast=str) 
    HASHING_ALGORITHM_LAYER_2: str = config("HASHING_ALGORITHM_LAYER_2", cast=str) 
    HASHING_SALT: str = config("HASHING_SALT", cast=str) 
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", cast=str) 
    SMTP_SERVER: str = config("SMTP_SERVER", cast=str) 
    SMTP_PORT: int = config("SMTP_PORT", default=587, cast=int) 
    SMTP_USERNAME: str = config("SMTP_USERNAME", cast=str) 
    SMTP_PASSWORD: str = config("SMTP_PASSWORD", cast=str) 
    SMTP_USE_TLS: bool = config("SMTP_USE_TLS", default=True, cast=bool) 
    SMTP_FROM_EMAIL: str = config("SMTP_FROM_EMAIL", default="no-reply@test.com", cast=str) 
    ROOT_DIR: pathlib.Path = ROOT_DIR 

    class Config: 
        case_sensitive: bool = True 
        env_file: str = f"{str(ROOT_DIR)}/.env" 
        validate_assignment: bool = True 
        extra = "allow" 

    @property 
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]: 
        return { 
            "title": self.TITLE, 
            "version": self.VERSION, 
            "debug": self.DEBUG, 
            "description": self.DESCRIPTION, 
            "docs_url": self.DOCS_URL, 
            "openapi_url": self.OPENAPI_URL, 
            "redoc_url": self.REDOC_URL, 
            "openapi_prefix": self.OPENAPI_PREFIX, 
            "api_prefix": self.API_PREFIX, 
        }

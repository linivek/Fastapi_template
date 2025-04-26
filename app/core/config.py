from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 项目设置
    PROJECT_NAME: str
    API_V1_STR: str

    # 服务器设置
    SERVER_HOST: str
    SERVER_PORT: int

    # 安全设置
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS设置
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 数据库设置
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int
    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        values = info.data
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Redis设置
    REDIS_SERVER: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: Optional[str] = None
    REDIS_URI: Optional[RedisDsn] = None

    @field_validator("REDIS_URI", mode="before")
    def assemble_redis_connection(cls, v: Optional[str], info) -> Any:
        if isinstance(v, str):
            return v
        # 构建Redis连接URI
        values = info.data
        redis_server = values.get("REDIS_SERVER", "")
        redis_port = values.get("REDIS_PORT", "")
        redis_db = values.get("REDIS_DB", "")
        redis_password = values.get("REDIS_PASSWORD")

        if redis_password:
            auth_part = f":{redis_password}@"
        else:
            auth_part = ""

        return f"redis://{auth_part}{redis_server}:{redis_port}/{redis_db}"

    # Celery配置
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_TIMEZONE: str
    CELERY_TASK_TRACK_STARTED: bool
    CELERY_TASK_TIME_LIMIT: int

    @field_validator("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND", mode="before")
    def assemble_celery_connection(cls, v: Optional[str], info) -> str:
        if isinstance(v, str):
            return v
        # 默认使用REDIS_URI
        values = info.data
        if values.get("REDIS_URI"):
            return values.get("REDIS_URI")

        # 手动构建连接
        redis_server = values.get("REDIS_SERVER", "")
        redis_port = values.get("REDIS_PORT", "")
        redis_db = values.get("REDIS_DB", "")
        redis_password = values.get("REDIS_PASSWORD")

        if redis_password:
            auth_part = f":{redis_password}@"
        else:
            auth_part = ""

        return f"redis://{auth_part}{redis_server}:{redis_port}/{redis_db}"

    # 初始超级用户配置
    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_USERNAME: Optional[str] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None

    # 时区配置
    TIME_ZONE: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000
    LOG_LEVEL: str = "DEBUG"

    PGPOOL_URLS: list[str] = [
        "postgresql+psycopg://postgres:postgres@localhost:5433/postgres",
        "postgresql+psycopg://postgres:postgres@localhost:5434/postgres",
    ]
    CASSANDRA_NODES: list[tuple[str, int]] = [
        ("localhost", 9042),
        ("localhost", 9043),
        ("localhost", 9044),
    ]

    REDIS_SENTINEL_NODES: list[tuple[str, int]] = [
        ("localhost", 26379),
        ("localhost", 26380),
        ("localhost", 26381),
    ]
    REDIS_MASTER_NAME: str = "redis-master"

    @field_validator("PGPOOL_URLS", mode="before")
    def convert_urla(cls, v):
        if isinstance(v[0], str):
            return v
        return [item.split(",") for item in v]

    @field_validator("CASSANDRA_NODES", "REDIS_SENTINEL_NODES", mode="before")
    def convert_nodes(cls, v):
        if isinstance(v[0], tuple):
            return v
        return [
            (
                item.split(":")[0],
                int(item.split(":")[1]),
            )
            for item in v
        ]

    SQLALCHEMY_ECHO: bool = True
    SQLALCHEMY_DB_POOL_SIZE: int = 100
    SQLALCHEMY_WEB_CONCURRENCY: int = 2

    def sqlalchemy_pool_size(self):
        return max(self.SQLALCHEMY_DB_POOL_SIZE // self.SQLALCHEMY_WEB_CONCURRENCY, 5)

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

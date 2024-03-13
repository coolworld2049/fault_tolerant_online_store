from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRESQL_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5434/postgres"
    )

    PGPOOL_NODES: list[int] | list[tuple[str, int]] = [
        ("localhost", 5432),
        ("localhost", 5433),
    ]

    CASSANDRA_NODES: list[int] | list[tuple[str, int]] = [
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

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

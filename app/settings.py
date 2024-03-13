from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRESQL_URL: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5434/postgres"
    )

    CASSANDRA_CONTACT_POINTS: list[int] | list[tuple[str, int]] = [
        ("localhost", 9042),
        ("localhost", 9043),
        ("localhost", 9044),
    ]
    CASSANDRA_KEYSPACE: str = "cassandra_keyspace"

    REDIS_SENTINEL_NODES: list[tuple[str, int]] = [("localhost", 26379)]
    REDIS_MASTER_NAME: str = "redismaster"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRESQL_URL: str = (
        "postgresql+psycopg2://postgres:adminpassword@localhost:5432/customdatabase"
    )

    CASSANDRA_CONTACT_POINTS: list[str] | list[tuple[str, int]] = [("localhost", 9042)]
    CASSANDRA_KEYSPACE: str = "cassandra_keyspace"

    REDIS_SENTINEL_NODES: list[tuple[str, int]] = [("localhost", 26379)]
    REDIS_MASTER_NAME: str = "redismaster"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()

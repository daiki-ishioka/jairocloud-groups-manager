from pydantic import computed_field
from pydantic_settings import BaseSettings


class RuntimeConfig(BaseSettings):
    """Configuration for runtime settings."""

    SECRET_KEY: str = "sample_secret_key"
    """A secret key for cryptographic operations."""

    POSTGRES_USER: str = "mapuser"
    """PostgreSQL database username."""

    POSTGRES_HOST: str = "localhost"
    """PostgreSQL database host."""

    POSTGRES_PASSWORD: str = "mappass"
    """PostgreSQL database password."""

    POSTGRES_DB: str = "mapdb"
    """PostgreSQL database name."""

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Database connection URI for SQLAlchemy."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/"
            f"{self.POSTGRES_DB}"
        )


config = RuntimeConfig()
"""runtime configuration instance."""

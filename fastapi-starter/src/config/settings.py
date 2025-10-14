from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env_file = BASE_DIR / "src" / "config" / ".env"


class Settings(BaseSettings):
    ENV: Literal["dev", "prod"] = "prod"
    ALLOWED_ORIGINS: str = ""
    SQLITE_PATH: Path = BASE_DIR / "src" / "infrastructure" / "db" / "database.db"

    model_config = SettingsConfigDict(env_file=env_file)

    @property
    def sqlite_path(self) -> Path:
        return Path(self.SQLITE_PATH)

    @property
    def allowed_origins(self) -> list[str]:
        return self.ALLOWED_ORIGINS.split(", ")


@lru_cache
def get_settings() -> Settings:
    return Settings()

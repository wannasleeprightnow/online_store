from dataclasses import dataclass
from os import environ
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv()


@dataclass
class PostgresDatabaseSettings:
    DATABASE_NAME: Optional[str] = environ.get("POSTGRES_NAME")
    HOST: Optional[str] = environ.get("POSTGRES_HOST")
    PORT: Optional[str] = environ.get("POSTGRES_PORT")
    USER: Optional[str] = environ.get("POSTGRES_USER")
    PASSWORD: Optional[str] = environ.get("POSTGRES_PASSWORD")
    DSN: str = (
        f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
    )


@dataclass
class AuthJWTSettings:
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 15
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    ALGORITHM: str = "RS256"
    PUBLIC_KEY: Path = BASE_DIR / "src" / "private_keys" / "jwt-public.pem"
    PRIVATE_KEY: Path = BASE_DIR / "src" / "private_keys" / "jwt-private.pem"


@dataclass
class ValidatorSettings:
    USERNAME_VALIDATE = re.compile(r"^[a-zA-Zа-яА-Я-]{1,50}$")
    NAME_VALIDATE = re.compile(r"^[а-яА-Я-]{1,25}$")
    PASSWORD_VALIDATE = re.compile(
        r"^(?=.*[a-zа-я])(?=.*[A-ZА-Я])(?=.*\d).{8,}$"
    )


@dataclass
class AppSettings:
    api_v1_prefix: str = "/api/v1"
    ALLOWED_ORIGINS: str = "127.0.0.1"

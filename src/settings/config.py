from dataclasses import dataclass, field
from datetime import timedelta

from authx import AuthXConfig, AuthX
from environs import Env

env = Env()
env.read_env()


@dataclass
class Settings:
    PG_USER: str = field(default_factory=lambda: env('PG_USER'))
    PG_PASS: str = field(default_factory=lambda: env('PG_PASS'))
    PG_HOST: str = field(default_factory=lambda: env('PG_HOST'))
    PG_PORT: int = field(default_factory=lambda: env('PG_PORT'))
    PG_NAME: str = field(default_factory=lambda: env('PG_NAME'))

    DEFAULT_ROLE: str = field(default_factory=lambda: env('DEFAULT_ROLE'))
    DEFAULT_ADMIN_NAME: str = field(default_factory=lambda: env('DEFAULT_ADMIN_NAME'))
    DEFAULT_ADMIN_PASSWORD: str = field(default_factory=lambda: env('DEFAULT_ADMIN_PASSWORD'))

    JWT_SECRET_KEY: str = field(default_factory=lambda: env("JWT_SECRET_KEY"))
    DEVELOP_MODE: str = field(default_factory=lambda: env("DEVELOP_MODE"))

    @property
    def DATABASE_URL(self) -> str:
        return f'postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_NAME}'

    def __post_init__(self):
        config = AuthXConfig()
        config.JWT_ACCESS_COOKIE_NAME = "auth_token"
        config.JWT_REFRESH_COOKIE_NAME = "refresh_token"
        config.JWT_TOKEN_LOCATION = ["cookies"]
        config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
        config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
        config.JWT_SECRET_KEY = self.JWT_SECRET_KEY
        config.JWT_COOKIE_SECURE = False
        config.JWT_COOKIE_SAMESITE = "lax"

        if self.DEVELOP_MODE == "dev":
            config.JWT_COOKIE_CSRF_PROTECT = False

        self.CONFIG = config
        self.SECURITY = AuthX(config=config)

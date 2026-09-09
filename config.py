from pydantic_settings import BaseSettings, SettingsConfigDict
from authx import AuthX , AuthXConfig
import os

if os.path.exists('.env'):
    with open('.env') as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///database.db"
    secret_key: str = os.getenv('secret_key', 'change_me')
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()


config = AuthXConfig()
config.JWT_SECRET_KEY = settings.secret_key
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False
security = AuthX(config = config)

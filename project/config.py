import os
from dataclasses import dataclass
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
from typing import MutableMapping, Any

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str

    def as_django_config_dict(self):
        return {
            'NAME': self.name,
            'USER': self.user,
            'PASSWORD': self.password,
            'HOST': self.host,
            'PORT': self.port,
        }


@dataclass(frozen=True)
class Config:
    BASE_DIR: Path
    APP_ENV: str
    DEBUG: bool
    SECRET_KEY: str
    DB: DatabaseConfig
    env: MutableMapping


def __from_env_var(key: str, default: Any = None) -> Any:
    if default is not None:
        return os.environ.get(key, default)
    return os.environ.get(key)


def _init_db_config() -> DatabaseConfig:
    db_host = __from_env_var('DB_HOST', 'localhost')
    db_port = __from_env_var('DB_PORT', 5432)
    db_name = __from_env_var('DB_NAME')
    db_user = __from_env_var('DB_USER')
    db_pass = __from_env_var('DB_PASS')
    return DatabaseConfig(db_host, db_port, db_name, db_user, db_pass)


def configuration_factory() -> Config:
    __env: MutableMapping = os.environ
    base_dir: Path = BASE_DIR
    app_env: str = __from_env_var('APP_ENV', 'prod')
    debug: bool = False if app_env == 'prod' else __from_env_var('DEBUG', False)
    secret_key: str = __from_env_var('SECRET_KEY')
    db = _init_db_config()
    return Config(base_dir, app_env, debug, secret_key, db, __env)


config: Config = configuration_factory()

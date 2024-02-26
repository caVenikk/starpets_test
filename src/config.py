import os
from dataclasses import dataclass
from functools import lru_cache

from environs import Env

DEFAULT_CONFIG_PATH = "./.env"


# Dataclass for the database configuration
@dataclass(frozen=True)
class Database:
    filename: str


# Dataclass for the weather API configuration
@dataclass(frozen=True)
class WeatherAPI:
    api_key: str


# Dataclass for the entire configuration
@dataclass(frozen=True)
class Config:
    database: Database
    weather_api: WeatherAPI


# Function to load the configuration from the environment
@lru_cache(maxsize=1)
def load_config(path: str | None = None) -> Config:
    if path is None:
        path = os.getenv("CONFIG_PATH", DEFAULT_CONFIG_PATH)

    env = Env()
    env.read_env(path)

    return Config(
        database=Database(
            filename=env.str("DB_FILENAME"),
        ),
        weather_api=WeatherAPI(
            api_key=env.str("WEATHER_API_KEY"),
        ),
    )

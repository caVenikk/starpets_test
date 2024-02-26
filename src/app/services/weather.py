import requests

from app.constants import (OPENWEATHER_COORDS_BASE_URL,
                           OPENWEATHER_WEATHER_BASE_URL)
from app.exceptions.weather import CityNotFoundError
from config import load_config

config = load_config()


# Function to get the coordinates of a given city
def get_coordinates(city: str, limit: int = 1) -> tuple[float, float]:
    response = requests.get(
        OPENWEATHER_COORDS_BASE_URL,
        params={"q": city, "limit": limit, "appid": config.weather_api.api_key},
    )

    data = response.json()
    if not data or response.status_code != 200:
        raise CityNotFoundError(city)

    return data[0]["lat"], data[0]["lon"]


# Function to fetch the weather data of a given city
def fetch_weather(city: str) -> dict:
    lat, lon = get_coordinates(city)

    response = requests.get(
        OPENWEATHER_WEATHER_BASE_URL,
        params={"lat": lat, "lon": lon, "units": "metric", "appid": config.weather_api.api_key},
    )

    if response.status_code != 200:
        raise CityNotFoundError(city)

    return response.json()

import aiohttp
from fastapi import HTTPException
import logging


class OpenWeatherFetcher:
    """Class implementation to fetch weather"""
    def __init__(self):
        pass

    @staticmethod
    async def fetch_latitude_longitude(city: str) -> tuple:
        """
        Fetch the latitude & longitude of city
        :param city: name of the city
        :return: latitude, longitude
        """
        logging.info("started")
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data.get('results', [])
                    if results:
                        return results[0].get('latitude'), results[0].get('longitude')
                    else:
                        logging.error(f"Empty response.")
                        return None, None
                else:
                    logging.error(f"Status code: {response.status}")
                    return None, None

    async def fetch_weather(self, city: str) -> dict:
        """
        Fetch weather for the given city
        :param city: name of the city
        :return: weather information
        """
        # Fetch latitude, longitude for city
        logging.info(f"fetching latitude & longitude for {city}")
        latitude, longitude = await self.fetch_latitude_longitude(city)

        if latitude is None or longitude is None:
            raise HTTPException(status_code=500, detail="Invalid City")

        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m'
        }
        logging.info(f"Fetching weather for lat:{latitude} & lon:{longitude}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    logging.debug(data)
                    return data
                else:
                    logging.error(f"Status code: {response.status}")
                    raise HTTPException(status_code=response.status, detail="Failed to fetch weather data")

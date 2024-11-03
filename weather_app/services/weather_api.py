import aiohttp
from fastapi import HTTPException


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
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    results = await data.get('results', [])
                    if results:
                        return results[0].get('latitude'), results[0].get('longitude')
                    else:
                        return None, None
                else:
                    return None, None

    async def fetch_weather(self, city: str) -> dict:
        """
        Fetch weather for the given city
        :param city: name of the city
        :return: weather information
        """
        # Fetch latitude, longitude for city
        latitude, longitude = await self.fetch_latitude_longitude(city)

        if latitude is None or longitude is None:
            raise HTTPException(status_code=500, detail="Invalid City")

        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': 'temperature_2m,relative_humidity_2m,cloud_cover,wind_speed_10m'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise HTTPException(status_code=response.status, detail="Failed to fetch weather data")

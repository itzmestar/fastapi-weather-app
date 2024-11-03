from weather_app.services.weather_api import OpenWeatherFetcher
from weather_app.services.storage import StorageService, S3StorageService
from weather_app.config.constants import S3_BUCKET


class WeatherService:
    def __init__(self, fetcher: OpenWeatherFetcher, storage: StorageService):
        self.fetcher = fetcher
        self.storage = storage

    async def get_weather(self, city: str) -> dict:
        """
        Get weather for the given city
        :param city: city name
        :return: weather data
        """

        weather_data = await self.fetcher.fetch_weather(city)
        storage_url = await self.storage.save_to_storage(city, weather_data)
        return weather_data


# Instantiate dependencies
fetcher = OpenWeatherFetcher()
storage = S3StorageService(S3_BUCKET)

weather_service = WeatherService(fetcher, storage)

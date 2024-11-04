from weather_app.services.weather_api import OpenWeatherFetcher
from weather_app.services.storage import StorageService, S3StorageService
from weather_app.services.event_logger import EventLogger, DynamoEventLogger
from weather_app.config.constants import S3_BUCKET, DYNAMODB_TABLE
from weather_app.services.cache_service import get_cached_weather
import time


class WeatherService:
    def __init__(self, fetcher: OpenWeatherFetcher, storage: StorageService, logger: EventLogger):
        self.fetcher = fetcher
        self.storage = storage
        self.logger = logger

    async def get_weather(self, city: str) -> dict:
        """
        Get weather for the given city
        :param city: city name
        :return: weather data
        """
        # check caches weather data if available then return the same
        cached_weather_data = await get_cached_weather(city, self.storage)
        if cached_weather_data:
            return cached_weather_data

        # fetch weather data
        weather_data = await self.fetcher.fetch_weather(city)
        # save to S3 bucket
        storage_url = await self.storage.save_to_storage(city, weather_data)
        # log the event in Dynamodb
        await self.logger.log_event(city, int(time.time()), storage_url)
        return weather_data


# Instantiate dependencies
fetcher = OpenWeatherFetcher()
storage = S3StorageService(S3_BUCKET)
event_logger = DynamoEventLogger(DYNAMODB_TABLE)

weather_service = WeatherService(fetcher, storage, event_logger)

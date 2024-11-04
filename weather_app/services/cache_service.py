import time
from weather_app.services.storage import StorageService


async def get_cached_weather(city: str, storage_service: StorageService) -> dict:
    """Check if cached weather data exists in S3 and is valid (within 5 minutes)."""
    # Take a note of current time
    now = time.time()

    # List all files in S3
    s3_files_list = await storage_service.list_files()

    # Filter files ending with json & starting with city name
    s3_files_list = [file for file in s3_files_list if file.endswith('.json') and file.startswith(f'{city}_')]

    # Search each file for 5min cache
    for file in s3_files_list:
        file_timestamp = int(file.split('_')[-1].replace('.json', ''))
        if now - file_timestamp < 300:
            # Fetch the cached weather
            cached_weather = await storage_service.get_file_content(file)
            return cached_weather
    # if cached weather is not found return None
    return None

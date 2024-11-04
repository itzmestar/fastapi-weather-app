from abc import ABC, abstractmethod
import aioboto3
import logging
from weather_app.config.constants import AWS_REGION
import uuid


class EventLogger(ABC):
    """Interface for EventLogger"""
    @abstractmethod
    async def log_event(self, city: str, timestamp: int, storage_url: str):
        pass


class DynamoEventLogger(EventLogger):
    """Implementation for DynamoEventLogger"""
    def __init__(self, dynamodb_table: str):
        self.dynamodb_table = dynamodb_table

    async def log_event(self, city: str, timestamp: int, storage_url: str):
        logging.info(f"Storing Event in dynamodb {self.dynamodb_table} table.")
        # Generate a unique EventId
        event_id = str(uuid.uuid4())
        logging.debug(f"EventId={event_id}, city={city}, timestamp={timestamp}, S3_url={storage_url}")
        async with aioboto3.Session().client('dynamodb', region_name=AWS_REGION) as dynamodb:
            await dynamodb.put_item(
                TableName=self.dynamodb_table,
                Item={
                    'EventId': {'S': event_id},  # Partition key
                    'city': {'S': city},
                    'timestamp': {'N': str(timestamp)},
                    'storage_url': {'S': storage_url}
                }
            )

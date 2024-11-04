from abc import ABC, abstractmethod
import aioboto3
import logging


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
        logging.debug(f"city={city}, timestamp={timestamp}, S3_url={storage_url}")
        async with aioboto3.Session().client('dynamodb') as dynamodb:
            await dynamodb.put_item(
                TableName=self.dynamodb_table,
                Item={
                    'city': city,
                    'timestamp': str(timestamp),
                    'S3_url': storage_url
                }
            )

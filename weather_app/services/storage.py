from abc import ABC, abstractmethod
import aioboto3
import json
import time


class StorageService(ABC):
    """Interface for StorageService"""
    @abstractmethod
    async def save_to_storage(self, city: str, data: dict) -> str:
        pass

    @abstractmethod
    async def list_files(self) -> list:
        pass

    @abstractmethod
    async def get_file_content(self, filename) -> dict:
        pass


class S3StorageService(StorageService):
    """Implementation for S3StorageService"""
    def __init__(self, s3_bucket: str):
        self.s3_bucket = s3_bucket

    async def save_to_storage(self, city: str, data: dict) -> str:
        """
        Save data to file on s3 bucket
        :param city: city name
        :param data: dict data
        :return: S3 url of saved file
        """
        timestamp = int(time.time())
        filename = f"{city}_{timestamp}.json"
        async with aioboto3.Session().client('s3') as s3_client:
            await s3_client.put_object(Bucket=self.s3_bucket, Key=filename, Body=json.dumps(data))
        return f"s3://{self.s3_bucket}/{filename}"

    async def list_files(self) -> list:
        """
        List the files in S3 bucket
        :return: list of files
        """
        async with aioboto3.Session().client('s3') as s3_client:
            response = await s3_client.list_objects_v2(Bucket=self.s3_bucket)
            return response.get('Contents', [])

    async def get_file_content(self, filename) -> dict:
        """
        Return content of file
        :param filename: filename in S3
        :return: json object
        """
        async with aioboto3.Session().client('s3') as s3_client:
            response = await s3_client.get_object(Bucket=self.s3_bucket, Key=filename)
            return json.loads(await response['Body'].read())
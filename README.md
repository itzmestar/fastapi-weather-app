# fastapi-weather-app
This is a simple weather API service using FastAPI that fetches weather
data from an external public API (https://open-meteo.com/). 
The service is designed to handle high traffic using asynchronous programming.

## Features

### 1. Asynchronous Data Fetching
Uses Python's `asyncio` to asynchronously fetch the current weather data from the
external API based on the `city` parameter.

### 2. AWS S3 Integration
- Each fetched weather response is stored as a JSON file in an S3 bucket.
- The filename is structured as `{city}_{timestamp}.json`.
- Uses asynchronous methods to upload the data to the S3.

### 3. AWS DynamoDB Integration:
- After storing the json file, it logs the event (with city name, timestamp, and S3 URL/local
path) into a DynamoDB table.
- Database interactions are performed using async methods.

### 4. Caching with S3:
- Before fetching the weather data from the external API, it checks if the data for the
requested city (fetched within the last 5 minutes) already exists in S3.
- If it exists, retrieves it directly without calling the external API.
- Cache is expired after 5 minutes.

## Installation

1. Clone the repository

```
git clone https://github.com/itzmestar/fastapi-weather-app
```

2. Change directory

```
cd fastapi-weather-app
```

3. Set these environment variables:

`AWS_ACCESS_KEY_ID,
AWS_SECRET_ACCESS_KEY,
S3_BUCKET`

4. Install requirements

```
pip3 install -r requirements.txt
```

### Run

```
uvicorn weather_app.main:app
```

## Using Docker

1. Clone the repository

```
git clone https://github.com/itzmestar/fastapi-weather-app
```

2. Change directory

```
cd fastapi-weather-app
```

3. Build docker image:
```
docker build -t fastapi-weather-app .
```

### Run docker container
```
docker run -e AWS_REGION=xx-xxxxx-x -e AWS_ACCESS_KEY_ID=AxxxxxxxxB -e AWS_SECRET_ACCESS_KEY=xxxxxxx -e S3_BUCKET=xxxxxx -e DYNAMODB_TABLE=xxxxxxxx -p 8000:8000 fastapi-weather-app
```

### Swagger GUI
Swagger GUI can be accessed at http://127.0.0.1:8000/docs

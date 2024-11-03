import logging.config
from fastapi import FastAPI

# get root logger
logger = logging.getLogger('weather_app')

app = FastAPI()


import logging.config
from fastapi import FastAPI

# setup loggers
logging.config.fileConfig('weather_app/config/logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger('weather_app')

app = FastAPI()


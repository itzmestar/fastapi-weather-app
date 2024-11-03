import logging.config
from fastapi import FastAPI
from weather_app.routers.router_weather import router as weather_router

# setup loggers
logging.config.fileConfig('weather_app/config/logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger('weather_app')

app = FastAPI()
app.include_router(weather_router)

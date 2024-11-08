from fastapi import APIRouter, HTTPException
from weather_app.services.weather_service import weather_service
from pydantic import BaseModel
import logging


# create an api-router
router = APIRouter(
    tags=["weather"],
)


class WeatherResponse(BaseModel):
    city: str
    weather: dict


@router.get("/weather/", response_model=WeatherResponse)
async def get_weather(
    city: str
):
    """
    Get weather info for the specified city
    """
    # make city name case insensitive
    city = city.lower()
    try:
        weather_data = await weather_service.get_weather(city)
        return WeatherResponse(city=city, weather=weather_data)
    except HTTPException as e:
        if e.status_code == 404:
            raise e
        else:
            raise HTTPException(status_code=500, detail="Something went wrong")
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=500, detail="Something went wrong")

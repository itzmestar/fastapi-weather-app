from fastapi import APIRouter


# create an api-router
router = APIRouter(
    tags=["weather"],
)


@router.get("/weather/")
async def get_weather(
    city: str
):
    """
    Get weather info for the specified city
    """
    return {
        'city': city
    }

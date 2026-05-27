import requests
from langchain.tools import tool
import os
import dotenv
dotenv.load_dotenv()

base = "http://api.openweathermap.org/data/2.5/weather"


@tool("get_weather", description="Get the current weather of a location")
def getWeather(location: str) -> str:
    print(f"Getting weather for {location}...")

    # api calling of weather
    api = requests.get(
        f"{base}?q={location}&appid={os.getenv('OPEN_WEATHER_API_KEY')}&units=metric")

    data = api.json()

    # return the data
    return data
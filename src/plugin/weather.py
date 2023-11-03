import requests
from dotenv import load_dotenv
import os

load_dotenv(".env.local")
open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")

def get_weather(api_key=open_weather_api_key, city="Hong%20Kong", country_code=''):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = f"""
            temperature: {data["main"]["temp"]},
            humidity: {data["main"]["humidity"]},
            wind_speed: {data["wind"]["speed"]},
            description: {data["weather"][0]["description"]},
        """
    return weather

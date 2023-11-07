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
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_description = data["weather"][0]["description"]
        weather = (
            f"temperature: {temp}, "
            f"humidity: {humidity}, "
            f"wind_speed: {wind_speed}, "
            f"description: {weather_description}"
        )
    else:
        weather = "Sorry, I can't get the weather for you."
    return weather

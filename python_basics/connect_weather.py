import requests
from dotenv import load_dotenv
import os 

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_COUNTRY_CODE = "in"
WEATHER_ZIP_CODE = "201007"


WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?zip={WEATHER_ZIP_CODE},{WEATHER_COUNTRY_CODE}&appid={WEATHER_API_KEY}"

response = requests.get(WEATHER_URL)

print(response.json())
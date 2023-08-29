import requests
import json
from app.settings import get_settings
from app.draw import draw_weather

settings = get_settings()


def get_weather_day(data_lat: str, data_lon: str):
    params = dict(key=settings.API_KEY, q=f'{data_lat},{data_lon}', days=1, aqi='no', alerts='no')
    res = requests.get(url='http://api.weatherapi.com/v1/forecast.json', params=params)
    return draw_weather(json.loads(res.text)['forecast']['forecastday'][0]['hour'])



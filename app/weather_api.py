import asyncio
import json
from aiohttp import ClientSession
from app.settings import get_settings
from app.draw import draw_weather

settings = get_settings()


async def get_weather_day(data_lat: str, data_lon: str):
    async with ClientSession() as session:
        params = dict(key=settings.API_KEY, q=f'{data_lat},{data_lon}', days=1, aqi='no', alerts='no')
        url = 'http://api.weatherapi.com/v1/forecast.json'

        async with session.get(url=url, params=params) as response:
            try:
                res = await response.json()
                start_time = int(res['location']['localtime'].split(' ')[-1].split(":")[0])
            except:
                return "Нет данных"
    return draw_weather(res['forecast']['forecastday'][0]['hour'][start_time:])




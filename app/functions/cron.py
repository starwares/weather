import os
from app import bot, dp, City
from aiogram.types import BufferedInputFile
from aiogram import types
from app.weather_api import get_weather_day


async def send_some(name, user_id):
    city_coat_of_arms = types.FSInputFile(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "cities",
                                                                       "uploads", "гербы", f'{name}.jpg')))
    await bot.send_photo(chat_id=user_id, photo=city_coat_of_arms, caption=f"Вы Выбрали город {name}")
    for city in City.city_list:
        if city.name == name:
            data_lat = city.data_lat
            data_lon = city.data_lon
            list_image = await get_weather_day(str(data_lat), str(data_lon))
            for image in list_image:
                await bot.send_photo(chat_id=user_id, photo=BufferedInputFile(image, filename='image.jpg'))
            break



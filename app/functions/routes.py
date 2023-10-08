import os
from app import bot, City
from app.weather_api import get_weather_day
from aiogram.types import BufferedInputFile
from aiogram import types


async def send_weather(message):
    city_coat_of_arms = types.FSInputFile(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "cities",
                                                                       "uploads", "гербы", f'{message.text}.jpg')))
    await bot.send_photo(chat_id=message.from_user.id, photo=city_coat_of_arms,
                         caption=f"Вы Выбрали город {message.text}")

    for city in City.city_list:
        if city.name == message.text:
            data_lat = city.data_lat
            data_lon = city.data_lon
            list_image = await get_weather_day(str(data_lat), str(data_lon))
            for image in list_image:
                await message.answer_photo(BufferedInputFile(image, filename='image.jpg'))
            break


async def send_weather_from_location(message):
    list_image = await get_weather_day(str(message.location.latitude), str(message.location.longitude))
    for image in list_image:
        await message.answer_photo(BufferedInputFile(image, filename='image.jpg'))

import os
from app import bot, City, scheduler
from aiogram.types import BufferedInputFile
from aiogram import types
from app.weather_api import get_weather_day
from app.crud import get_cron, create_cron, get_all_cron, delete_cron


async def start_load_cron():
    all_cron = await get_all_cron()
    for cron in all_cron:
        scheduler.add_job(send_some, "cron", id=cron.id, hour=str(cron.hour), minute='*/' + str(cron.minutes),
                          args=[cron.city_name,
                                cron.user_id, ])
    scheduler.start()


# отрисовка погоды для задачи хранящейся в БД
async def send_some(name, user_id):
    city_coat_of_arms = types.FSInputFile(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "cities",
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


# Проверка на существование cron для этого пользователя
async def creation_request(user_id):
    result = await get_cron(user_id)
    if result:
        return False
    return True


# создание задачи для пользователя
async def create(user_id: str, city_name: str, hour: int, minutes: int):
    existence_check = await creation_request(user_id)
    if not existence_check:
        return False
    else:
        cron = await create_cron(user_id, city_name, hour, minutes)
        return cron


async def delete(user_id: str):
    cron_id = await delete_cron(user_id)
    return cron_id



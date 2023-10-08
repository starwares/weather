import os

from aiogram.filters.command import Command
from app.menu import markup as nav
from app.functions.routes import send_weather_from_location, send_weather
from aiogram import types, F
from app import dp, City, bot, scheduler
import asyncio
from app.crud import get_all_cron
from app.cities.main import start_uploads
from app.functions.cron import send_some


@dp.message(Command('cities'))
async def cities(message: types.Message):
    await message.answer("Выберите букву с которой начинается интересующий Вас город России"
                         " или напишите его название",
                         reply_markup=nav.alphabet_menu.as_markup(resize_keyboard=True),
                         )


@dp.message(Command("location"))
async def cmd_special_buttons(message: types.Message):
    await message.answer(
        "Погода по текущей геолакации.",
        reply_markup=nav.location.as_markup(resize_keyboard=True),
    )


@dp.message(Command("crones"))
async def cmd_crones(message: types.Message):
    await message.answer("В этом меню Вы можете создать или удалить ежедневное автоматическое сообщение о погоде",
                         reply_markup=nav.cron_menu.as_markup(resize_keyboard=True),
                         )


@dp.message(F.location)
async def on_user_location(message: types.Message):
    await send_weather_from_location(message)


@dp.message(F.text)
async def on_city(message: types.Message):
    if message.text == "Создать":
        pass

    if message.text in City.dict_RU.keys():
        alpha_menu = nav.create_menu(key=message.text)
        await message.answer("Выберите или напишите букву с которой начинается интересующий Вас город России",
                             reply_markup=alpha_menu.as_markup(resize_keyboard=True),
                             )
    elif message.text in City.arr_RU:
        cities_menu = nav.create_menu(cities=City.cities_by_first_letter[message.text])
        await message.answer(f'Города на буква {message.text}',
                             reply_markup=cities_menu.as_markup(resize_keyboard=True),)
    elif message.text in City.cities_by_first_letter[message.text[0]]:
        await send_weather(message)


async def main():
    all_cron = await get_all_cron()
    for cron in all_cron:
        scheduler.add_job(send_some, "cron", id=cron.id, hour=str(cron.hour), minute='*/'+str(cron.minutes), args=["Москва",
                                                                                               cron.user_id, ])
    City.city_list = await start_uploads()
    City.cities = [city.name for city in City.city_list]
    for letter in City.arr_RU:
        City.cities_by_first_letter[letter] = [city for city in City.cities if city.startswith(letter)]
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

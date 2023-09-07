import os
import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import BufferedInputFile
from aiogram.filters.command import Command
from app.cities.main import start_uploads
from app.crud import get_all_cron
from app.settings import get_settings
import markup as nav


from app.weather_api import get_weather_day
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()
settings = get_settings()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

arr_RU = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
          'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']


async def send_some(name, user_id):
    city_coat_of_arms = types.FSInputFile(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "cities",
                                                                       "uploads", "гербы", f'{name}.jpg')))
    await bot.send_photo(chat_id=user_id, photo=city_coat_of_arms, caption=f"Вы Выбрали город {name}")
    for city in city_list:
        if city.name == name:
            data_lat = city.data_lat
            data_lon = city.data_lon
            list_image = await get_weather_day(str(data_lat), str(data_lon))
            for image in list_image:
                await bot.send_photo(chat_id=user_id, photo=BufferedInputFile(image, filename='image.jpg'))
            break


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


@dp.message(F.location)
async def on_user_location(message: types.Message):
    list_image = await get_weather_day(str(message.location.latitude), str(message.location.longitude))
    for image in list_image:
        await message.answer_photo(BufferedInputFile(image, filename='image.jpg'))


@dp.message(F.text)
async def on_city(message: types.Message):
    if message.text in nav.dict_RU.keys():
        alpha_menu = nav.create_menu(key=message.text)
        await message.answer("Выберите или напишите букву с которой начинается интересующий Вас город России",
                             reply_markup=alpha_menu.as_markup(resize_keyboard=True),
                             )
    elif message.text in arr_RU:
        cities_menu = nav.create_menu(cities=cities_by_first_letter[message.text])
        await message.answer(f'Города на буква {message.text}',
                             reply_markup=cities_menu.as_markup(resize_keyboard=True),)
    elif message.text in cities_by_first_letter[message.text[0]]:
        city_coat_of_arms = types.FSInputFile(os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "cities",
                                                                           "uploads", "гербы", f'{message.text}.jpg')))
        await bot.send_photo(chat_id=message.from_user.id, photo=city_coat_of_arms, caption=f"Вы Выбрали город {message.text}")

        for city in city_list:
            if city.name == message.text:
                data_lat = city.data_lat
                data_lon = city.data_lon
                list_image = await get_weather_day(str(data_lat), str(data_lon))
                for image in list_image:
                    await message.answer_photo(BufferedInputFile(image, filename='image.jpg'))
                break


async def main():
    all_cron = await get_all_cron()
    for cron in all_cron:
        scheduler.add_job(send_some, "cron", hour=str(cron.hour), minute='*/'+str(cron.minutes), args=["Москва",
                                                                                                       cron.user_id, ])
    city_list[:] = await start_uploads()
    cities[:] = [city.name for city in city_list]
    for letter in arr_RU:
        cities_by_first_letter[letter] = [city for city in cities if city.startswith(letter)]
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    # Создаем словарь, где ключами являются буквы алфавита, а значениями - списки городов начинающихся на эту букву
    cities_by_first_letter = {}
    # Создаем список городов
    city_list = []
    cities = []
    asyncio.run(main())


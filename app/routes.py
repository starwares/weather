from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from app.menu import markup as nav
from app.functions.routes import send_weather_from_location, send_weather
from aiogram import types, F
from app import dp, City, bot, scheduler, start_load_cities
from app.functions.cron import start_load_cron, delete as delete_cron
import asyncio
from app.menu.dialog import Form

from app.functions.cron import send_some, create


@dp.message(Command('start'))
async def cities(message: types.Message):
    await message.answer("Добро пожаловать, Вы можете использовать команды:"
                         " /cities - для выбора города,"
                         " /location - для просмотра по локации, "
                         "/crones - для ежедневного оповещения")


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


@dp.message(Form.city_name)
async def process_name(message: types.Message, state: FSMContext):
    if message.text[0] in City.arr_RU:

        if message.text in City.cities_by_first_letter[message.text[0]]:
            await state.update_data(city_name=message.text)
            await message.answer(
                "Введите во сколько часов вы хотите получать сообщение: Пример: 21")
            await state.set_state(Form.hour)
    else:
        await message.answer(
            "Вашего города нет в базе, попробуйте еще раз...")
        await state.set_state(Form.city_name)


@dp.message(Form.hour)
async def process_name(message: types.Message, state: FSMContext):
    if 0 <= int(message.text) <= 24:
        await state.update_data(hour=int(message.text))
        await message.answer(
            "Введите во сколько минут вы хотите получать сообщение: Пример: 0")
        await state.set_state(Form.minutes)
    else:
        await message.answer(
            "Вы ввели невозможное число, попробуйте еще раз...")
        await state.set_state(Form.hour)


@dp.message(Form.minutes)
async def process_name(message: types.Message, state: FSMContext):
    if 0 <= int(message.text) <= 60:
        await state.update_data(minutes=int(message.text))
        user_data = await state.get_data()
        cron = await create(user_id=str(message.from_user.id), city_name=user_data["city_name"], hour=user_data["hour"], minutes=user_data["minutes"])
        if not cron:
            await message.answer(
                "У Вас уже есть задача для выполнения, удалите старую для создания новой")
        else:
            scheduler.add_job(send_some, "cron", id=cron.id, hour=str(cron.hour), minute='*/' + str(cron.minutes),
                              args=[cron.city_name,
                                    cron.user_id, ])
            await state.clear()
            await message.answer(
                "Задача успешно создана!")


@dp.message(F.location)
async def on_user_location(message: types.Message):
    await send_weather_from_location(message)


@dp.message(F.text)
async def on_city(message: types.Message, state: FSMContext):
    if message.text in City.dict_RU.keys():
        alpha_menu = nav.create_menu(key=message.text)
        await message.answer("Выберите или напишите букву с которой начинается интересующий Вас город России",
                             reply_markup=alpha_menu.as_markup(resize_keyboard=True),
                             )
    elif message.text in City.arr_RU:
        cities_menu = nav.create_menu(cities=City.cities_by_first_letter[message.text])
        await message.answer(f'Города на буква {message.text}',
                             reply_markup=cities_menu.as_markup(resize_keyboard=True),)
    elif message.text[0] in City.arr_RU:
        if message.text in City.cities_by_first_letter[message.text[0]]:
            await send_weather(message)
    elif message.text == "Удалить":
        cron_id = await delete_cron(str(message.from_user.id))
        if cron_id:
            scheduler.remove_job(cron_id)
            await message.answer(
                "Ваша задача успешно удалена!")
        else:
            await message.answer(
                "Ваша задача не удалена, попробуйте позже!")
    if message.text == "Создать":
        await message.answer(
            "Вам нужно ввести имя города!")
        await state.set_state(Form.city_name)


async def main():
    await start_load_cities()
    await start_load_cron()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

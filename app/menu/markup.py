from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from app import City

alphabet_menu = ReplyKeyboardBuilder()

for alpha in City.dict_RU.keys():
    alphabet_menu.add(types.KeyboardButton(text=alpha))

alphabet_menu.adjust(3)

location = ReplyKeyboardBuilder()

location.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))

cron_menu = ReplyKeyboardBuilder()
cron_menu.add(types.KeyboardButton(text="Создать"))
cron_menu.add(types.KeyboardButton(text="Удалить"))


def create_menu(key: str | None = None, cities: list | None = None):
    new_menu = ReplyKeyboardBuilder()
    if key:
        some_list = City.dict_RU[key]
    else:
        some_list = cities
    for element in some_list:
        new_menu.add(types.KeyboardButton(text=element))
    new_menu.adjust(3)
    return new_menu





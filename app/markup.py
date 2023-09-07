from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

dict_RU = {'А - Г': ['А', 'Б', 'В', 'Г'], 'Д - Ж': ['Д', 'Е', 'Ё', 'Ж'], 'З - К': ['З', 'И', 'Й', 'К'],
           'Л - О': ['Л', 'М', 'Н', 'О'], 'П - Т': ['П', 'Р', 'С', 'Т'], 'У - Ц': ['У', 'Ф', 'Х', 'Ц'],
           'Ч - Щ': ['Ч', 'Ш', 'Щ'], 'Э - Я': ['Э', 'Ю', 'Я']}


alphabet_menu = ReplyKeyboardBuilder()

for alpha in dict_RU.keys():
    alphabet_menu.add(types.KeyboardButton(text=alpha))

alphabet_menu.adjust(3)

location = ReplyKeyboardBuilder()

location.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))


def create_menu(key: str | None = None, cities: list | None = None):
    new_menu = ReplyKeyboardBuilder()
    if key:
        some_list = dict_RU[key]
    else:
        some_list = cities
    for element in some_list:
        new_menu.add(types.KeyboardButton(text=element))
    new_menu.adjust(3)
    return new_menu





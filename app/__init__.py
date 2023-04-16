import requests
import string
import telebot
from telebot import types

bot = telebot.TeleBot('6025211553:AAEiqx3SooJR-pQGwqsqD0mYtg6urup_F1c')



# Сортировка списка городов по алфавиту



# Создание клавиатуры с городами
# def create_city_keyboard():
#     keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     for city in cities:
#         keyboard.add(city)
#     return keyboard
#
#
# # Обработчик команды /start
# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = create_city_keyboard()
#     bot.send_message(message.chat.id, "Выберите город из списка:", reply_markup=markup)
#
#
# # Обработчик сообщений с городами
# @bot.message_handler(func=lambda message: message.text in cities)
# def city_selected(message):
#     # set_user_city(message.chat.id, message.text)
#     markup = telebot.types.ReplyKeyboardRemove(selective=False)
#     bot.send_message(message.chat.id, "Город {} выбран.".format(message.text), reply_markup=markup)


# Создаем список городов
cities = {
    'Москва': 'Moscow',
    'Санкт-Петербург': 'Saint Petersburg',
    'Новосибирск': 'Novosibirsk',
    'Екатеринбург': 'Yekaterinburg',
    'Нижний Новгород': 'Nizhny Novgorod',
    'Казань': 'Kazan',
    'Омск': 'Omsk',
    'Челябинск': 'Chelyabinsk',
    'Ростов-на-Дону': 'Rostov-on-Don',
    'Уфа': 'Ufa',
    'Волгоград': 'Volgograd',
    'Пермь': 'Perm',
    'Красноярск': 'Krasnoyarsk',
    'Воронеж': 'Voronezh',
    'Саратов': 'Saratov',
    'Краснодар': 'Krasnodar'
}


# Создаем словарь, где ключами являются буквы алфавита, а значениями - списки городов начинающихся на эту букву
cities_by_first_letter = {}
for letter in string.ascii_uppercase:
    cities_by_first_letter[letter] = [city for city in cities if city.startswith(letter)]

# Функция, которая создает клавиатуру с городами, начинающимися на заданную букву
def create_city_keyboard(letter):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for city in cities_by_first_letter[letter]:
        button = types.InlineKeyboardButton(text=city, callback_data=city)
        keyboard.add(button)
    return keyboard

# Функция, которая создает клавиатуру с буквами алфавита
def create_alphabet_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=13)
    for letter in string.ascii_uppercase:
        button = types.InlineKeyboardButton(text=letter, callback_data=letter)
        keyboard.add(button)
    return keyboard

# Обработчик нажатий на кнопки с буквами алфавита
@bot.callback_query_handler(lambda query: query.data in string.ascii_uppercase)
def handle_alphabet_query(query):
    letter = query.data
    keyboard = create_city_keyboard(letter)
    bot.send_message(chat_id=query.message.chat.id, text=f"Города на букву {letter}:", reply_markup=keyboard)

# Обработчик команды /cities
@bot.message_handler(commands=['cities'])
def handle_cities_command(message):
    keyboard = create_alphabet_keyboard()
    bot.send_message(chat_id=message.chat.id, text="Выберите букву алфавита:", reply_markup=keyboard)




# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, '<b>Привет Лиза</b>', parse_mode='html')
#
#
# @bot.message_handler()
# def get_user_text(message):
#     bot.send_message(message.chat.id, message, parse_mode='html')


bot.polling(none_stop=True)

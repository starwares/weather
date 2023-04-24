import os

import requests
import string
import telebot
from telebot import types
from app.cities.main import start_uploads
from app.crud import add_city_to_user

bot = telebot.TeleBot('6025211553:AAEiqx3SooJR-pQGwqsqD0mYtg6urup_F1c')

# Создаем список городов
cities = start_uploads()

arr_RU = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я'];

# Создаем словарь, где ключами являются буквы алфавита, а значениями - списки городов начинающихся на эту букву
cities_by_first_letter = {}
for letter in arr_RU:
    cities_by_first_letter[letter] = [city for city in cities if city.startswith(letter)]


@bot.message_handler(commands=['cities'])
def cities(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for letter in arr_RU:
        markup.add(types.InlineKeyboardButton(text=letter, callback_data=letter))
    bot.send_message(message.chat.id, "Выберите букву с которой начинается интересующий Вас город России", reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data in arr_RU:
            markup = types.InlineKeyboardMarkup(row_width=2)
            for city in cities_by_first_letter[call.data]:
                markup.add(types.InlineKeyboardButton(text=city, callback_data=city))
            bot.send_message(call.message.chat.id, f'Города на буква {call.data}', reply_markup=markup)
        elif call.data in cities_by_first_letter[call.data[0]]:

            bot.send_photo(call.message.chat.id, photo=open(os.path.abspath(os.path.join(os.path.abspath(__file__),
                                                                                         "..", "cities", "uploads",
                                                                                         "гербы", f'{call.data}.jpg')),
                                                            'rb'), caption=f"Вы Выбрали город {call.data}")


if __name__ == "__main__":
    bot.polling(none_stop=True)

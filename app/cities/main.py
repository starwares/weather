import os
from bs4 import BeautifulSoup
import time
from typing import List
import multiprocessing
import requests
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from app.crud import add_city_in_db

def download_coat_of_arms_of_the_city(image_url_and_city_name: tuple):
    path = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "uploads", "гербы"))

    image_url, city_name = image_url_and_city_name
    # Выполняем HTTP-запрос на получение герба города
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Сохраняем герб на диск
        with open(f'{path}/{city_name}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)


def multi_download_pool(city_with_coat_of_arms_list: List):
    start = time.time()
    pool = Pool(processes=multiprocessing.cpu_count())
    for city_with_coat_of_arms in city_with_coat_of_arms_list:
        pool.apply_async(download_coat_of_arms_of_the_city, args=city_with_coat_of_arms)
    pool.close()
    pool.join()
    end = time.time()
    print(end - start)


def multi_download_thread(city_with_coat_of_arms_list: List):
    start = time.time()
    pool = ThreadPool(processes=100)
    pool.map(download_coat_of_arms_of_the_city, city_with_coat_of_arms_list)
    pool.close()
    pool.join()
    end = time.time()
    print(end - start)


def fill_in_data():
    path = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "uploads", "гербы"))

    # Создаем папку для сохранения гербов
    if not os.path.exists(path):
        os.makedirs(path)

    # Список городов с гербами еще не скаченных
    city_with_coat_of_arms_list = []

    # Ссылка на страницу со списком городов России на Википедии
    url = 'https://ru.wikipedia.org/wiki/Список_городов_России'

    # Выполняем HTTP-запрос на получение HTML-кода страницы
    response = requests.get(url)

    # Используем BeautifulSoup для парсинга HTML-кода страницы
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим таблицу со списком городов и их гербами
    table = soup.find('table', {'class': 'standard sortable'})

    # Список Всех городов
    cities: List = []



    # Проходим по каждой строке таблицы, содержащей информацию о городах
    for row in table.find_all('tr')[1:]:
        # Извлекаем название города и ссылку на его герб
        columns = row.find_all('td')
        city_name = columns[2].text.strip()
        if city_name.endswith("не призн."):
            city_name = city_name[:-9]
        image_url = 'https:' + columns[1].find('img')['src']
        cities.append(city_name)
        # Проверка на существование файла
        if not os.path.isfile(f'{path}/{city_name}.jpg'):
            city_with_coat_of_arms_list.append((image_url, city_name))

    return city_with_coat_of_arms_list, cities


def start_uploads():
    city_with_coat_of_arms_list, cities = fill_in_data()
    # multi_download_pool(city_with_coat_of_arms_list)

    add_city_in_db([i[1] for i in city_with_coat_of_arms_list])
    multi_download_thread(city_with_coat_of_arms_list)
    return cities


# start_uploads()

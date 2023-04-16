import os
from bs4 import BeautifulSoup
import time
from typing import List
import multiprocessing
import requests
from multiprocessing import Pool


# Ссылка на страницу со списком городов России на Википедии
url = 'https://ru.wikipedia.org/wiki/Список_городов_России'

# Выполняем HTTP-запрос на получение HTML-кода страницы
response = requests.get(url)

# Используем BeautifulSoup для парсинга HTML-кода страницы
soup = BeautifulSoup(response.text, 'html.parser')

# Находим таблицу со списком городов и их гербами
table = soup.find('table', {'class': 'standard sortable'})


def download_coat_of_arms_of_the_city(image_url: str, city_name: str):
    # Выполняем HTTP-запрос на получение герба города
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        # Сохраняем герб на диск
        with open(f'uploads/гербы/{city_name}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
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


# Создаем папку для сохранения гербов
if not os.path.exists('uploads/гербы'):
    os.makedirs('uploads/гербы')

# Список городов с гербами еще не скаченных
city_with_coat_of_arms_list = []


# Проходим по каждой строке таблицы, содержащей информацию о городах
for row in table.find_all('tr')[1:]:
    # Извлекаем название города и ссылку на его герб
    columns = row.find_all('td')
    city_name = columns[2].text.strip()
    image_url = 'https:' + columns[1].find('img')['src']
    # Проверка на существование файла
    if not os.path.isfile(f'uploads/гербы/{city_name}.jpg'):
        city_with_coat_of_arms_list.append((image_url, city_name))


multi_download_pool(city_with_coat_of_arms_list)





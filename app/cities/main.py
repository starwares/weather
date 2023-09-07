import os
from bs4 import BeautifulSoup
import time
from typing import List
import multiprocessing
import requests
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from app.crud import add_city_in_db, get_city_maplink
from app.schemas import City
import asyncio

city_list = []


def download_coat_of_arms_of_the_city(city: City):
    path = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "uploads", "гербы"))
    # Выполняем HTTP-запрос на получение герба города
    response = requests.get(city.image_url, stream=True)
    if response.status_code == 200:
        # Сохраняем герб на диск
        with open(f'{path}/{city.name}.jpg', 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)


def parsing_maplink(city: City):
    try:
        response_city = requests.get(city.url)
        soup_city = BeautifulSoup(response_city.text, 'html.parser')
        maplink_for_city = soup_city.find("a", {'class': 'mw-kartographer-maplink'})
        city.data_lat = maplink_for_city['data-lat']
        city.data_lon = maplink_for_city['data-lon']
    except Exception as e:
        print(f"{city.name} не удалось узнать кординаты. Ошибка: {e}")


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
    pool = ThreadPool(processes=10)
    pool.map(download_coat_of_arms_of_the_city, city_with_coat_of_arms_list)
    pool.close()
    pool.join()
    end = time.time()
    print(f"download: {end - start}")


def multi_parsing_thread(cities: List):
    start = time.time()
    pool = ThreadPool(processes=10)
    pool.map(parsing_maplink, cities)
    pool.close()
    pool.join()
    end = time.time()
    print(f"parsing: {end - start}")


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

    # Проходим по каждой строке таблицы, содержащей информацию о городах
    for row in table.find_all('tr')[1:]:
        # Извлекаем название города и ссылку на его герб
        columns = row.find_all('td')
        city_name = columns[2].text.strip()
        if city_name.endswith("не призн."):
            city_name = city_name[:-9]
        city_url = columns[2].find('a', href=True)
        # Заходим на страницу города и ищем его кординаты
        if city_url:
            city_url = f"https://ru.wikipedia.org{city_url['href']}"
            for city in city_list:
                if city.name == city_name:
                    break
            else:
                city = City(id='', name=city_name, image_url='https:' + columns[1].find('img')['src'],
                                      url=city_url, data_lat='', data_lon='')
                city_list.append(city)
                # Проверка на существование файла
                if not os.path.isfile(f'{path}/{city_name}.jpg'):
                    city_with_coat_of_arms_list.append(city)
    multi_parsing_thread(city_with_coat_of_arms_list)

    return city_with_coat_of_arms_list


async def start_uploads():
    city_with_coat_of_arms_list = fill_in_data()
    # multi_download_pool(city_with_coat_of_arms_list)

    await add_city_in_db(city_with_coat_of_arms_list)
    multi_download_thread(city_with_coat_of_arms_list)
    return await get_city_maplink(city_list)




async def main():
    new = await start_uploads()
    print(new)
    print("werverv")


if __name__ =="__main__":
    asyncio.run(main())



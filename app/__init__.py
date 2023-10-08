
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from app.cities.main import start_uploads
from app.settings import get_settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()
scheduler.start()
storage = MemoryStorage()
settings = get_settings()

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


class City:
    dict_RU = {'А - Г': ['А', 'Б', 'В', 'Г'], 'Д - Ж': ['Д', 'Е', 'Ё', 'Ж'], 'З - К': ['З', 'И', 'Й', 'К'],
               'Л - О': ['Л', 'М', 'Н', 'О'], 'П - Т': ['П', 'Р', 'С', 'Т'], 'У - Ц': ['У', 'Ф', 'Х', 'Ц'],
               'Ч - Щ': ['Ч', 'Ш', 'Щ'], 'Э - Я': ['Э', 'Ю', 'Я']}

    arr_RU = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
              'Ф',
              'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я']
    # Создаем словарь, где ключами являются буквы алфавита, а значениями - списки городов начинающихся на эту букву
    cities_by_first_letter = {}
    # Создаем список городов
    city_list = []
    cities = []


async def start_load_cities():
    City.city_list = await start_uploads()
    City.cities = [city.name for city in City.city_list]
    for letter in City.arr_RU:
        City.cities_by_first_letter[letter] = [city for city in City.cities if city.startswith(letter)]





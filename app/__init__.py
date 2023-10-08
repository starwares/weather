

from aiogram import Bot, Dispatcher


from app.settings import get_settings

from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()
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









from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    city_name = State()
    hour = State()
    minutes = State()


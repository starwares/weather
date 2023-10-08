from typing import Dict, Any
import asyncio
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Checkbox, Button, Row, Start, Cancel
from aiogram_dialog import Dialog, DialogManager, setup_dialogs
from app.crud import get_cron


async def getter(dialog_manager: DialogManager, **kwargs) -> Dict[str, Any]:
    if dialog_manager.find(EXTEND_BTN_ID).is_checked():
        return {
            "extended_str": "on",
            "extended": True,
        }
    else:
        return {
            "extended_str": "off",
            "extended": False,
        }


class MainMenu(StatesGroup):
    START = State()
    user_id = None

    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__()


class Settings(StatesGroup):
    START = State()


EXTEND_BTN_ID = "extend"


def create_window(user_id: str):
    pass


window = Window(
    Format(
        "Привет, {event.from_user.username}. \n\n"
    ),
    Const(
        "Вы точно хотите удалить все планировщики?",
        when="extended",
    ),
    Row(
        Checkbox(
            checked_text=Const("[x] Удалить Все"),
            unchecked_text=Const("[ ] Удалить Все"),
            id=EXTEND_BTN_ID,
        ),
        Start(Const("Settings"), id="settings", state=Settings.START),
    ),
    getter=getter,
    state=MainMenu.START
)
NOTIFICATIONS_BTN_ID = "notify"
ADULT_BTN_ID = "adult"

next_menu = Dialog(
    Window(
        Format("m"),
        Checkbox(
            checked_text=Const("[x] Send notifications"),
            unchecked_text=Const("[ ] Send notifications"),
            id=NOTIFICATIONS_BTN_ID,
        ),
        Checkbox(
            checked_text=Const("[x] Adult mode"),
            unchecked_text=Const("[ ] Adult mode"),
            id=ADULT_BTN_ID,
        ),
        Row(
            Cancel(),
            Cancel(text=Const("Save"), id="save"),
        ),
        state=Settings.START,
    )
)

main_menu = Dialog(window)



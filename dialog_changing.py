import operator
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Url, Column, Group, Select, Checkbox, ManagedCheckbox, Multiselect, Radio
from aiogram_dialog.widgets.text import Const, Format, List #Here we will import widgets we need
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.api.entities import MediaAttachment
from environs import Env
from pprint import pprint

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


class StartSG(StatesGroup):
    window_1 = State()
    window_2 = State()
    window_3 = State()
    window_4 = State()

class SecondDialogSG(StatesGroup):
    start = State()

async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()

async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

async def start_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=SecondDialogSG.start)

async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    if dialog_manager.start_data:
        getter_data = {'username': event_from_user.username or 'Stranger',
                       'first_show': True}
        dialog_manager.start_data.clear()
    else:
        getter_data = {'first_show': True}
    return getter_data

start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n', when='first_show'),
        Const('It is <b>the first</b> window of the dialog'),
        Button(Const('Next'), id='b_next', on_click=go_next),
        getter=username_getter,
        state=StartSG.window_1
    ),
    Window(
        Const('It is <b>the second</b> window of the dialog'),
        Row(
            Button(Const('Back'), id='b_back', on_click=go_back),
            Button(Const('Next'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const('It is <b>the third</b> window of the dialog'),
        Row(
            Button(Const('Back'), id='b_back', on_click=go_back),
            Button(Const('Next'), id='b_next', on_click=go_next),
        ),
        state=StartSG.window_3
    ),
    Window(
        Const('It is <b>the fourth</b> window of the dialog'),
        Row(
            Button(Const('Back'), id='b_back', on_click=go_back),
        ),
        state=StartSG.window_4
    ),
)

second_dialog = Dialog(
        Window(
        Const('Нажми на кнопку,\nчтобы вернуться в стартовый диалог 👇'),
        Button(Const('Кнопка'), id='button_start', on_click=go_start),
        state=SecondDialogSG.start
    ),
)

@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=StartSG.window_1,
        mode=StartMode.RESET_STACK, 
        data={'first_show': True}
    )


if __name__ == '__main__':
    dp.include_router(router)
    dp.include_routers(start_dialog, second_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
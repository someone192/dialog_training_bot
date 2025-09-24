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
    start = State()

class SecondDialogSG(StatesGroup):
    start = State()

async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

async def start_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=SecondDialogSG.start)

async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    print(f'dialog_start_data={dialog_manager.start_data}')
    return {'username':event_from_user.username or 'Stranger'}

start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('Нажми на кнопку,\nчтобы перейти во второй диалог 👇'),
        Button(Const('Кнопка'), id='go_second', on_click=start_second),
        getter=username_getter,
        state=StartSG.start
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
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK, data={'my_data':'my_data'})


if __name__ == '__main__':
    dp.include_router(router)
    dp.include_routers(start_dialog, second_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
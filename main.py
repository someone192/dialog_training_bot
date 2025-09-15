from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.text import Const #Here we will import widgets we need
from environs import Env

env = Env()
env.read_env()

bot_token = env('BOT_TOKEN')
dp = Dispatcher()

class StartSG(StatesGroup):
    start = State()

async def some_handler(callback: CallbackQuery, dialog_manager: DialogManager): #There will be handlers here
    pass

async def some_getter(**kwargs): #We will create getters here
    pass
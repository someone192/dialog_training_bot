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

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default= DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

class StartSG(StatesGroup):
    start = State()

async def some_handler(callback: CallbackQuery, dialog_manager: DialogManager): #There will be handlers here
    pass

async def some_getter(**kwargs): #We will create getters here
    pass

#It is a start dialog
start_dialog = Dialog(
    Window(
        #we will add widgets and getters here
    ),
)

@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

dp.include_router(start_dialog)
setup_dialogs(dp)
dp.run_polling(bot)
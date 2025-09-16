from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const, Format #Here we will import widgets we need
from environs import Env
from pprint import pprint

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default= DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()

class StartSG(StatesGroup):
    start = State()

async def yes_click_process(callback: CallbackQuery,
                            widget: Button,
                            dialog_manager: DialogManager): #There will be handlers here
    await callback.message.edit_text(
        text='<b>Прекрасно!</b>\n\nНадеюсь, вы найдете в этом курсе что-то '
             'новое и полезное для себя!'
    )
    await dialog_manager.done()


async def no_click_process(callback: CallbackQuery,
                           widget: Button, 
                           dialog_manager: DialogManager):
    await callback.message.edit_text(
        text='<b>Попробуйте!</b>\n\nСкорее всего, вам понравится!'
    )
    await dialog_manager.done()


async def username_getter(event_from_user: User, **kwargs): #We will create getters here dialog_manager: DialogManager, event_from_user: User, 
    pprint(kwargs)
    return {'username': event_from_user.username}

#It is a start dialog
start_dialog = Dialog(
    Window(
        Format(text='Привет, <b>{username}</b>!\n'),
        Const(
            text='Пробовали ли вы уже писать ботов с использованием '
                 'библиотеки <code>aiogram_dialog</code>?'
        ),
        Row(
            Button(text=Const('✅ Да'), id='yes', on_click=yes_click_process),
            Button(text=Const('✖️ Нет'), id='no', on_click=no_click_process)
        ),
        getter=username_getter,
        state=StartSG.start
        #we will add widgets and getters here
    ),
)

@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

if __name__ == '__main__':
    dp.include_router(router)
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
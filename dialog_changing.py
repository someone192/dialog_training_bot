import operator
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs, ShowMode
from aiogram_dialog.widgets.kbd import Button, Row, Url, Column, Group, Select, Checkbox, ManagedCheckbox, Multiselect, Radio, Back, Next
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
    first = State()
    second = State()

async def close_second_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()

# async def go_first(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.switch_to(state=StartSG.window_1)

# async def go_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.switch_to(state=StartSG.window_2)

# async def go_third(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.switch_to(state=StartSG.window_3)

# async def go_fourth(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#     await dialog_manager.switch_to(state=StartSG.window_4)

async def go_back(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()

async def go_next(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.next()


async def go_start(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.window_1, mode=StartMode.RESET_STACK)

async def go_second_dialog(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.start(state=SecondDialogSG.first)

async def switch_to_first_one(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=StartSG.window_1)

async def switch_to_first_two(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=StartSG.window_2)

async def switch_to_first_three(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=StartSG.window_3)

async def switch_to_first_four(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=StartSG.window_4)

async def switch_to_second_one(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=SecondDialogSG.first)

async def switch_to_second_two(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.switch_to(state=SecondDialogSG.second)


#async def switch_to_second(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
#    await dialog_manager.start(state=SecondDialogSG.second)

async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    getter_data = {'username': event_from_user.username or 'Stranger'}
    return getter_data

start_dialog = Dialog(
    Window(
        Format('<b>Привет, {username}!</b>\n'),
        Const('It is <b>the first</b> window of the dialog, choose window you want to go'),
        Const('Or press the button to start new dialog'),
        Row(
            Button(Const('2'), id='b_second', on_click=switch_to_first_two),
            Button(Const('3'), id='b_third', on_click=switch_to_first_three),
            Button(Const('4'), id='b_fourth', on_click=switch_to_first_four),
        ),
        Row(
            Button(Const('Next'), id='b_next', on_click=go_next),
        ),
        Row(
            Button(Const('New dialog'), id='go_second', on_click=go_second_dialog),
        ),
        getter=username_getter,
        state=StartSG.window_1
    ),
    Window(
        Const('It is <b>the second</b> window of the dialog'),
        Row(
            Button(Const('1'), id='b_first', on_click=switch_to_first_one),
            Button(Const('3'), id='b_third', on_click=switch_to_first_three),
            Button(Const('4'), id='b_fourth', on_click=switch_to_first_four),
        ),
        Row(
            Button(Const('Back'), id='b_back', on_click=go_back),
            Button(Const('Next'), id='b_next', on_click=go_next),
        ),
        Row(
            Button(Const('New dialog'), id='go_second', on_click=go_second_dialog),
        ),
        state=StartSG.window_2
    ),
    Window(
        Const('It is <b>the third</b> window of the dialog'),
        Row(
            Button(Const('1'), id='b_first', on_click=switch_to_first_one),
            Button(Const('2'), id='b_second', on_click=switch_to_first_two),
            Button(Const('4'), id='b_fourth', on_click=switch_to_first_four),
        ),
        Row(
            Back(Const('Back'), id='back'),
            Next(Const('Next'), id='next'),
        ),      
        Row(
            Button(Const('New dialog'), id='go_second', on_click=go_second_dialog),
        ),
        state=StartSG.window_3
    ),
    Window(
        Const('It is <b>the fourth</b> window of the dialog'),
        Row(
            Button(Const('1'), id='b_first', on_click=switch_to_first_one),
            Button(Const('2'), id='b_second', on_click=switch_to_first_two),
            Button(Const('3'), id='b_third', on_click=switch_to_first_three),
        ),
        Row(
            Button(Const('Back'), id='b_back', on_click=go_back),
        ),
        Row(
            Button(Const('New dialog'), id='go_second', on_click=go_second_dialog),
        ),
        state=StartSG.window_4
    ),
)

second_dialog = Dialog(
    Window(
        Const('Нажми на кнопку,\nчтобы вернуться в стартовый диалог or to go to second window 👇'),
        Button(Const('Second window'), id='w_second', on_click=switch_to_second_two),
        Button(Const('First_dialog'), id='first_dialog', on_click=close_second_dialog),
        state=SecondDialogSG.first
    ),

    Window(
        Const('You are in the second window of second dialog\npress the button to return to first dialog or the first window'),
        Button(Const('Button'), id='w_first', on_click=switch_to_second_one),
        Button(Const('First dialog'), id='first_dialog', on_click=close_second_dialog),
        state=SecondDialogSG.second
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
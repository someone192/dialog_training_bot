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

bot = Bot(token=BOT_TOKEN, default= DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()

class StartSG(StatesGroup):
    start = State()
    #con1 = State()

'''
# Это хэндлер, срабатывающий на нажатие кнопки с категорией товаров
async def category_selection(callback: CallbackQuery, widget: Select,
                             dialog_manager: DialogManager, item_id: str):
    print(f'Выбрана категория с id={item_id}')


async def checkbox_clicked(callback: CallbackQuery, checkbox: ManagedCheckbox,
                           dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(is_checked=checkbox.is_checked())


# Это геттер
async def get_categories(**kwargs):
    categories = [
        ('Техника', 1),
        ('Одежда', 2),
        ('Обувь', 3),
    ]
    return {'categories': categories}


async def getter(dialog_manager: DialogManager, **kwargs):
    checked=dialog_manager.dialog_data.get('is_checked')
    return{
        'checked':checked,
        'not_checked':not checked
        }


async def get_topics(dialog_manager: DialogManager, **kwargs):
    topics = [
        ("IT", '1'),
        ("Дизайн", '2'),
        ("Наука", '3'),
        ("Общество", '4'),
        ("Культура", '5'),
        ("Искусство", '6'),
    ]
    return {'topics':topics}

async def media_getter(**kwargs):
    photo = MediaAttachment(type=ContentType.PHOTO, url='https://telegra.ph/file/ac76e3f1551f7d59de970.jpg')
    return {'photo':photo}
'''


def age_check(text: str)-> str:
    if all(ch.isdigit() for ch in text) and 3 <= int(text) <= 120:
        return text
    raise ValueError


async def correct_age_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        text: str
)-> None:
    await message.answer(text=f'Вам {text}')


async def error_age_handler(
        message: Message,
        widget: ManagedTextInput,
        dialog_manager: DialogManager,
        error: ValueError                                           
)-> None:
    await message.answer(text='Вы ввели некорректный возраст. Попробуйте еще раз')

async def message_handler(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
)-> None:
    dialog_manager.show_mode = ShowMode.NO_UPDATE
    await message.send_copy(message.chat.id)


async def no_text(
        message: Message,
        widget: MessageInput,
        dialog_manager: DialogManager
):
    print(type(widget))
    await message.answer(text='It is not a text, give me a text you shit')

'''async def get_languages(dialog_manager:DialogManager, **kwargs):
    checked=dialog_manager.find('radio_lang').get_checked()
    language = {
        '1': 'en',
        '2': 'ru',
        '3': 'fr'
    }
    chosen_lang = language['2' if not checked else checked]
    lang = {
        'ru': {
            '1': '🇬🇧 Английский',
            '2': '🇷🇺 Русский',
            '3': '🇫🇷 Французский',
            'text': 'Выберите язык'
        },
        'en': {
            '1': '🇬🇧 English',
            '2': '🇷🇺 Russian',
            '3': '🇫🇷 French',
            'text': 'Choose language'
        },
        'fr': {
            '1': '🇬🇧 Anglais',
            '2': '🇷🇺 Russe',
            '3': '🇫🇷 Français',
            'text': 'Choisissez la langue'
        }
    }
    languages = [
        (f"{lang[chosen_lang]['1']}", '1'),
        (f"{lang[chosen_lang]['2']}", '2'),
        (f"{lang[chosen_lang]['3']}", '3'),
    ]
    return{'languages': languages,
           'text': lang[chosen_lang]['text']}

start_dialog = Dialog(
    Window(
        Format(text='{text}'),
        Column(
            Radio(
                checked_text=Format('🔘 {item[0]}'),
                unchecked_text=Format('⚪️ {item[0]}'),
                id='radio_lang',
                item_id_getter=operator.itemgetter(1),
                items='languages',
            ),
        ),
        state=StartSG.start,
        getter=get_languages
    )
)'''

'''start_dialog = Dialog(
    Window(
        Const(text='Отметьте темы новостей 👇'),
        Column(
            Multiselect(
                checked_text=Format('[✔️] {item[0]}'),
                unchecked_text=Format('[  ] {item[0]}'),
                id='multi_topics',
                item_id_getter=operator.itemgetter(1),
                items='topics',
                min_selected=2,
                max_selected=4,
            ),
        ),
        state=StartSG.start,
        getter=get_topics
    ),
)'''

start_dialog = Dialog(
    Window(
        Const(text='Write down your age'),
        TextInput(
            id='age_input',
            type_factory=age_check,
            on_success=correct_age_handler,
            on_error=error_age_handler,
        ),
        MessageInput(
            func=no_text,
            content_types=ContentType.ANY,
        ),
    state=StartSG.start,
    ),
)

@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)

#@router.message(Command(commands='con1'))
#async def command_start_process(message: Message, dialog_manager: DialogManager):
#    await dialog_manager.start(state=StartSG.con1)


if __name__ == '__main__':
    dp.include_router(router)
    dp.include_router(start_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)
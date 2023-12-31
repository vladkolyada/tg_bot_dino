from aiogram import types
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from aiogram.types import ParseMode

from utils.misc.throttling import rate_limit
from loader import dp, db_sqlite, bot
from keyboards.inline.default_inline_keyboards import start_keyboard
from data.config import ADMINS
from states.steps import StatesForBot


@rate_limit(limit=5, key="/start")
@dp.message_handler(CommandStart())
async def start_command(message: types.Message):
    await StatesForBot.UsualState.set()
    db_sqlite.add_new_user(id=message.chat.id, first_name=message.chat.first_name,
                           last_name=message.chat.last_name, nickname=message.chat.username)
    await message.answer_photo(photo=open("images/start_image.jpg", 'rb'),
                               caption='"Доісторичні хижаки" - перший в Україні освітній проєкт про скам`янілості '
                                       'динозаврів, який співпрацює із загальноосвітніми навчальними закладами. \n\n'
                                       'Виставка скам`янілостей динозаврів приїжджає в навчальний заклад з '
                                       'пізнавальною екскурсією. А самим цікавим є те, що до скам`янілостей учні '
                                       'мають змогу доторкнутися! \n\n'
                                       'З 2023 року проєкт має декілька тематичних виставок: '
                                       '\n1. "Морські та літаючі хижаки". Відвідавши її, ви зможете познайомитися '
                                       'з зубами мегалодона та мозазавра, скам`янілостями археоптерикса '
                                       'та птеродактиля і т. д. '
                                       '\n2. "Наземні хижаки". Серед цікавих експонатів цієї виставки проєкту - '
                                       'череп знаменитого велоцираптора, зуби спінозавра, '
                                       'кігті мегараптора та багато іншого. \n\n'
                                       ' А головною перлиною нашого проєкту є перша в Україні, анатомічно коректна '
                                       'модель правої половини черепа тиранозавра в натуральний розмір '
                                       '(довжина 130 см.). \n\n'
                                       'Також, дуже скоро, очікуємо на поповнення нашої колекції. '
                                       'На даний момент працюємо над розробкою третьої виставки під назвою '
                                       '"Травоїдні захисники".',
                               reply_markup=start_keyboard, parse_mode=ParseMode.HTML)


@dp.message_handler(commands=['notify_all'], state=StatesForBot.UsualState)
async def notify_all_users(message: types.Message):
    for user_admin in ADMINS:
        if message.chat.id == user_admin:
            text_for_notify = message.text[11:]
            users_sqlite = db_sqlite.get_users()
            for user_sqlite in users_sqlite:
                try:
                    await bot.send_message(chat_id=user_sqlite[0], text=text_for_notify, parse_mode=ParseMode.HTML)
                    if int(user_sqlite[1]) != 1:
                        db_sqlite.set_users_active(id=user_sqlite[0], active=1)
                except:
                    db_sqlite.set_users_active(id=user_sqlite[0], active=0)

            await message.answer(text="Вдала розсилка!")
        else:
            pass


@dp.message_handler(commands=['notify_all_with_picture'], state=StatesForBot.UsualState)
async def notify_all_users_with_picture(message: types.Message):
    for user_admin in ADMINS:
        if message.chat.id == user_admin:
            await StatesForBot.AfterCommandNotifyAllWithPicture.set()
            await message.answer(text='Відправте своє фото з описом(текст під фото)')
    else:
        pass


@dp.message_handler(content_types=ContentType.PHOTO, state=StatesForBot.AfterCommandNotifyAllWithPicture)
async def get_photo_and_caption(message: types.Message):
    for user_admin in ADMINS:
        if message.chat.id == user_admin and message.content_type == types.ContentType.PHOTO:
            photo = message.photo[-1]
            caption = message.caption

            users_sqlite = db_sqlite.get_users()
            for user_sqlite in users_sqlite:
                try:
                    await bot.send_photo(chat_id=user_sqlite[0], photo=photo.file_id, caption=caption,
                                         parse_mode=ParseMode.HTML)
                    if int(user_sqlite[1]) != 1:
                        db_sqlite.set_users_active(id=user_sqlite[0], active=1)
                except:
                    db_sqlite.set_users_active(id=user_sqlite[0], active=0)
            await message.answer(text="Вдала розсилка!")

            await StatesForBot.UsualState.set()
        else:
            pass



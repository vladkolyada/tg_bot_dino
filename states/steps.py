from aiogram.dispatcher.filters.state import StatesGroup, State


class StatesForBot(StatesGroup):
    UsualState = State()
    AfterCommandNotifyAllWithPicture = State()

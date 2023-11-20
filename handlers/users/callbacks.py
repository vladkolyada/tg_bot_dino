from aiogram import types

from loader import dp, db, bot
from states.steps import StatesForBot
from keyboards.inline.default_inline_keyboards import social_medias_keyboard


@dp.callback_query_handler(state=StatesForBot.UsualState)
async def callbacks(callback: types.CallbackQuery):
    if callback.data == "social_medias":
        await callback.message.answer(text="Підписуйтеся на наші соціальні мережі ⬇️",
                                      reply_markup=social_medias_keyboard)


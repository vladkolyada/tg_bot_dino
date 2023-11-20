from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Поїхали!", callback_data="social_medias")
    ]
])

social_medias_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Youtube", url="https://www.youtube.com/@Dinosaur2023"),
        InlineKeyboardButton(text="Instagram", url="https://instagram.com/timko.sergii?igshid=aXo4OTY4a3Z2dTZq")
    ],
    [
        InlineKeyboardButton(text="Замовити приїзд проєкту в навчальний заклад",
                             url="https://www.instagram.com/direct/t/17848766366949304")
    ]
])

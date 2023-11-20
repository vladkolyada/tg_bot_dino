import logging

from data.config import ADMINS


async def on_startup_notify(dp):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=admin, text="Bot is started")
        except Exception as err:
            logging.exception(err)
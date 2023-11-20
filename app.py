from aiogram import executor

from loader import dp, db_sqlite
import middlewares, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await on_startup_notify(dispatcher)
    # notifies about bot start

    try:
        db_sqlite.create_table()
    except Exception as err:
        print(err)
    # create table if not exists

    await set_default_commands(dispatcher)
    # set default commands


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

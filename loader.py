from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.database import DataBase
from utils.db_api.data_base_sqlite import DataBaseSqlite


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase()
db_sqlite = DataBaseSqlite("utils/db_api/datab.db")

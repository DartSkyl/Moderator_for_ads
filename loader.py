from typing import List

from base import BotBase
from config import BOT_TOKEN, DB_INFO, MAIN_GROUP_ID, ADMINS_LIST

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


db = BotBase(DB_INFO[0], DB_INFO[1], DB_INFO[2], DB_INFO[3])

bot = Bot(token=BOT_TOKEN, parse_mode="HTML", disable_web_page_preview=True)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

# В этом списке будем хранить ID всех администраторов
admins_id: List[int] = ADMINS_LIST


async def db_connect():
    """В этой функции идет подключение к БД и проверка ее структуры"""
    await db.connect()
    await db.check_db_structure()


# async def admin_list_load():
#     """Функция заносит в список ID администраторов из основной группы при включении бота."""
#     admins = await bot.get_chat_administrators(chat_id=MAIN_GROUP_ID)
#     admins = {admin.user.id for admin in admins}
#     for admin_id in admins:
#         admins_id.append(admin_id)

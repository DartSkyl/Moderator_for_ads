import asyncio
import datetime
import handlers  # noqa
from loader import dp, db_connect, bot, admin_list_load
from utils import admin_router, users_router


async def start_up():
    #  Подключаем свои роутеры
    dp.include_router(admin_router)
    dp.include_router(users_router)
    #  Подключаемся к базе
    await db_connect()
    #  Загружаем ID администраторов прямо из основной группы
    await admin_list_load()

    # Стартуем! Я начну стрелять!
    # with open('bot.log', 'a') as log_file:
    #     log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await dp.start_polling(bot,
                           # allowed_updates=[
                           #     "message",
                           #     "callback_query",
                           #     "pre_checkout_query",
                           #     "chat_member"
                           # ]
                           )


if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')

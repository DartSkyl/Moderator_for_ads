import asyncio
import datetime
import handlers  # noqa
from loader import dp, db_connect, bot, admin_list_load, bot
from utils import (admin_router, users_router, create_publisher, queue_for_moderation, queue_for_publication)
from aiogram.types.bot_command import BotCommand


async def start_up():
    #  Подключаем свои роутеры
    await create_publisher()
    dp.include_router(admin_router)
    dp.include_router(users_router)
    #  Подключаемся к базе
    await db_connect()
    #  Загружаем ID администраторов прямо из основной группы
    await admin_list_load()
    # Запускаем очередь на модерацию
    await queue_for_moderation.load_queue_from_base()
    await queue_for_publication.load_queue_from_base()
    await bot.set_my_commands(commands=[BotCommand(command='start',
                                                   description='Нажать для начала взаимодействия или рестарта')])
    # Стартуем! Я начну стрелять!
    with open('bot.log', 'a') as log_file:
        log_file.write(f'\n========== New bot session {datetime.datetime.now()} ==========\n\n')
    print('Стартуем')
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')

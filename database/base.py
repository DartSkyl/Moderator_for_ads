import time
from typing import List
import asyncpg as apg
from asyncpg import Record


class BotBase:
    """Через данный класс реализованы конект с базой данных и методы взаимодействия с БД"""

    def __init__(self, _db_user, _db_pass, _db_name, _db_host):
        self.db_name = _db_name
        self.db_user = _db_user
        self.db_pass = _db_pass
        self.db_host = _db_host
        self.pool = None

    async def connect(self):
        """Для использования БД будем использовать пул соединений.
        Иначе рискуем поймать asyncpg.exceptions._base.InterfaceError: cannot perform operation:
        another operation is in progress. А нам это не надо"""
        self.pool = await apg.create_pool(
            database=self.db_name,
            user=self.db_user,
            password=self.db_pass,
            host=self.db_host,
            max_inactive_connection_lifetime=10,
            min_size=1,
            max_size=100
        )

    async def check_db_structure(self) -> None:
        # Таблица со всеми группами
        async with self.pool.acquire() as connection:
            pass

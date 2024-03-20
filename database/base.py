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
        async with self.pool.acquire() as connection:
            # self.container_id = container_id
            # self.text = text
            # self.file_id = file_id
            # self.user_id = user_id
            # self.public_time = public_time
            # self.validity = validity

            await connection.execute("CREATE TABLE IF NOT EXISTS mod_queue"
                                     "(container_id VARCHAR(10) PRIMARY KEY,"
                                     "text TEXT,"
                                     "file_id TEXT,"
                                     "user_id BIGINT,"
                                     "public_time VARCHAR(20));")

            await connection.execute("CREATE TABLE IF NOT EXISTS pub_queue"
                                     "(container_id VARCHAR(10) PRIMARY KEY,"
                                     "text TEXT,"
                                     "file_id TEXT,"
                                     "user_id BIGINT,"
                                     "public_time VARCHAR(20),"
                                     "time_index BIGINT);")
            pass

    async def input_ads_mod(self, container_id: str, text: str, file_id: str, user_id: int, public_time: str):
        """Добавляем контейнер в таблицу модерации"""
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO public.mod_queue (container_id, text, file_id, user_id, public_time) VALUES ('{container_id}', '{text}', '{file_id}', {user_id}, '{public_time}');")

    async def remove_ads_mod(self, container_id: str):
        """Удаляем контейнер по ID"""
        async with self.pool.acquire() as connection:
            await connection.execute(f"DELETE FROM public.mod_queue WHERE container_id = '{container_id}';")

    async def output_queue_mod(self):
        """Выгружаем очередь публикаций"""
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM public.mod_queue")
            return result

    async def input_ads_pub(self, container_id: str, text: str, file_id: str, user_id: int, public_time: str, time_index: int):
        """Добавляем контейнер в таблицу модерации"""
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO public.pub_queue"
                                     f"(container_id, text, file_id, user_id, public_time, time_index)"
                                     f"VALUES ('{container_id}', '{text}', '{file_id}', {user_id}, '{public_time}', {time_index})"
                                     f"ON CONFLICT (container_id) DO UPDATE SET public_time = '{public_time}', time_index = {time_index};")

    async def remove_ads_pub(self, container_id: str):
        """Удаляем контейнер по ID"""
        async with self.pool.acquire() as connection:
            await connection.execute(f"DELETE FROM public.pub_queue WHERE container_id = '{container_id}';")

    async def output_queue_pub(self):
        """Выгружаем очередь публикаций"""
        async with self.pool.acquire() as connection:
            result = await connection.fetch(f"SELECT * FROM public.pub_queue")
            return result


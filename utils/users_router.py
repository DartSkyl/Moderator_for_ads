from typing import List
from loader import admins_id
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsNotAdminFilter(BaseFilter):
    """Фильтр, проверяющий является ли отправитель сообщения админом"""
    def __init__(self, admins_list: List[int]):

        # Список ID администраторов загружается прямо
        # из основной группы во время запуска бота
        self.admins_list = admins_list

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id not in self.admins_list


users_router = Router()
users_router.message.filter(IsNotAdminFilter(admins_list=admins_id))

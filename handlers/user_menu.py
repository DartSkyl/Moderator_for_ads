from utils import users_router

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asyncpg.exceptions import UniqueViolationError


@users_router.message(Command('start'))
async def start_function(msg: Message):
    """Функция запускается при старте бота и вводе соответствующей команды от имени пользователя"""
    await msg.answer(text='Привет, пользователь!')

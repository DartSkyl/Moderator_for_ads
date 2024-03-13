from utils import admin_router

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asyncpg.exceptions import UniqueViolationError


@admin_router.message(Command('start'))
async def start_function(msg: Message):
    """Функция запускается при старте бота и вводе соответствующей команды от имени администратора"""
    await msg.answer(text='Привет, админ!')

from utils import admin_router, queue_for_moderation
from keyboards import main_admin_keyboard, admin_cancel

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from asyncpg.exceptions import UniqueViolationError


@admin_router.message(Command('start'))
async def start_function(msg: Message):
    """Функция запускается при старте бота и вводе соответствующей команды от имени администратора"""
    await msg.answer(
        text=f'Привет, {html.quote(msg.from_user.first_name)}!\nЖду ваших решений😉',
        reply_markup=main_admin_keyboard
    )


@admin_router.message(F.text == '📋 Очередь объявлений на модерацию')
async def view_queue_for_moderation(msg: Message):
    """Здесь начинается просмотр очереди на модерацию"""
    await queue_for_moderation.get_ads_from_queue()
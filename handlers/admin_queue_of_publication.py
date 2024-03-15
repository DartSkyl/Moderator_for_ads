from utils import admin_router, queue_for_publication
from keyboards import main_admin_keyboard, moderation_keyboard, admin_file, admin_back
from states import ModerationAds
from loader import bot

from aiogram.types import Message, FSInputFile
from aiogram import F, html
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder


@admin_router.message(F.text == '📰 Очередь объявлений на публикацию')
async def view_queue_for_publication(msg: Message, state: FSMContext):
    """Здесь начинается просмотр очереди на публикацию"""
    ads_list = await queue_for_publication.get_ads_list()
    if not isinstance(ads_list, str):
        for ads in ads_list:
            print(ads)

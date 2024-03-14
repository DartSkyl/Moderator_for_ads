from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder

from loader import bot


async def editing_function(ads, from_user_id):
    """Даная функция позволяет корректировать объявления"""
    # Превью
    # Редактировать текст
    # редактировать фото
    # редактировать время публикации
    # редактировать время действия
    # отправить на модерацию
    # удалить объявление + подтверждение либо отказ в публикации (стандартный текст + комментарий)

    if ads.file_id:
        media_group = MediaGroupBuilder(caption=ads.text)
        for mediafile in ads.file_id:
            media_group.add(type=mediafile[1], media=mediafile[0])
        await bot.send_media_group(chat_id=from_user_id, media=media_group.build())

    # else:

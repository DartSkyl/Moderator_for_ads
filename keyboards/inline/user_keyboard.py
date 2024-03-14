from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup


async def content_selection():
    """Клавиатура для выбора содержания будущего объявления"""
    buttons = [  # Так как текст присутствует везде, то кроме чистого текста будем помечать так
        [InlineKeyboardButton(text='Текст', callback_data='text')],
        [InlineKeyboardButton(text='Текст + Фото', callback_data='photo')],
        [InlineKeyboardButton(text='Текст + Видео', callback_data='video')],
        [InlineKeyboardButton(text='🚫 Отмена', callback_data='cancel')]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

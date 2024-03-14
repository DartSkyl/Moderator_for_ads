from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_buttons = [
        [KeyboardButton(text='📋 Очередь объявлений на модерацию')],
        [KeyboardButton(text='📰 Очередь объявлений на публикацию')],
        [KeyboardButton(text='📝 Создать пост')]
]

main_admin_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )


admin_cancel = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='🚫 Отмена')]],
        resize_keyboard=True,
)


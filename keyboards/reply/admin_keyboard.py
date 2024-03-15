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

moderation_keyboard = ReplyKeyboardMarkup(
        keyboard=[
                [KeyboardButton(text='Отправить на публикацию')],
                [KeyboardButton(text='Редактировать текст'),
                 KeyboardButton(text='Редактировать фото/видео')],
                [KeyboardButton(text='Редактировать время публикации'),
                 KeyboardButton(text='Редактировать время действия')],
                [KeyboardButton(text='Удалить объявление')]
        ],
        resize_keyboard=True
)


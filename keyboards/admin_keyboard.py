from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup


async def rm_channel_keys(channels_list):
    ch_keys = InlineKeyboardBuilder()
    for c in channels_list:
        ch_keys.button(text=f'{c[1]}', callback_data=f'rm_id_{c[0]}')
    ch_keys.adjust(1)
    return ch_keys.as_markup()


channel_mang = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Добавить канал')],
              [KeyboardButton(text='Удалить канал')],
              [KeyboardButton(text='Вернуться в главное меню')]],
    resize_keyboard=True
)

kb_buttons = [
    [KeyboardButton(text='📋 Очередь объявлений на модерацию')],
    [KeyboardButton(text='📰 Очередь объявлений на публикацию')],
    [KeyboardButton(text='📝 Создать пост'), KeyboardButton(text='📣 Каналы для публикаций')]
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

admin_back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Назад')]],
    resize_keyboard=True,
)

admin_file = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Дальше ▶️')],
              [KeyboardButton(text='◀️ Назад')]],
    resize_keyboard=True)

admin_create_file = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Дальше ▶️')],
              [KeyboardButton(text='🚫 Отмена')]],
    resize_keyboard=True
)

admin_back_2 = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Вернуться')]],
    resize_keyboard=True,
)

admin_file_2 = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Дальше ▶️')],
              [KeyboardButton(text='◀️ Вернуться')]],
    resize_keyboard=True)

moderation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить на публикацию')],
        [KeyboardButton(text='Редактировать текст'),
         KeyboardButton(text='Редактировать фото/видео')],
        [KeyboardButton(text='Редактировать время публикации'), ],
        [KeyboardButton(text='Отказать в публикации'),
         KeyboardButton(text='Вернуться в главное меню')]
    ],
    resize_keyboard=True
)

admin_preview_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить на публикацию')],
        [KeyboardButton(text='Редактировать текст'),
         KeyboardButton(text='Редактировать фото/видео')],
        [KeyboardButton(text='Редактировать время публикации')],
        [KeyboardButton(text='Удалить объявление')]
    ],
    resize_keyboard=True
)

admin_no_time = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Опубликовать сразу')]],
    resize_keyboard=True
)

view_queue = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='◀️ Предыдущее объявление'),
         KeyboardButton(text='Следующее объявление ▶️')],
        [KeyboardButton(text='Редактировать объявление')],
        [KeyboardButton(text='Вернуться в главное меню')]
    ],
    resize_keyboard=True
)

confirm = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='✅ Да'), KeyboardButton(text='Нет ❌')]
    ],
    resize_keyboard=True
)

edit_public_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Редактировать текст'),
         KeyboardButton(text='Редактировать фото/видео')],
        [KeyboardButton(text='Редактировать время публикации')],
        [KeyboardButton(text='Удалить объявление')],
        [KeyboardButton(text='Вернуться в очередь на публикацию')]
    ],
    resize_keyboard=True
)

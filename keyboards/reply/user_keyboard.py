from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_buttons = [
        [KeyboardButton(text='📝 Создать объявление')],
        [KeyboardButton(text='📨 Связь с администрацией')]
]

main_user_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )


user_cancel = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='🚫 Отмена')]],
        resize_keyboard=True
)

user_back = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Назад')]],
        resize_keyboard=True
)

user_no_time = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Опубликовать сразу')]],
    resize_keyboard=True
)


user_file = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Дальше ▶️')],
                  [KeyboardButton(text='🚫 Отмена')]],
        resize_keyboard=True
)

user_file_2 = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Дальше ▶️')],
                  [KeyboardButton(text='◀️ Назад')]],
        resize_keyboard=True
)

preview_keyboard = ReplyKeyboardMarkup(
        keyboard=[
                [KeyboardButton(text='Отправить на модерацию')],
                [KeyboardButton(text='Редактировать текст'),
                 KeyboardButton(text='Редактировать фото/видео')],
                [KeyboardButton(text='Редактировать время публикации')],
                [KeyboardButton(text='Удалить объявление')]
        ],
        resize_keyboard=True
)

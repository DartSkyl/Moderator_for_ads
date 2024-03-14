from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_buttons = [
        [KeyboardButton(text='📝 Создать объявление')],
        [KeyboardButton(text='📂 Мои объявления')],
        [KeyboardButton(text='📨 Связь с администрацией')]
]

main_user_keyboard = ReplyKeyboardMarkup(
        keyboard=kb_buttons,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )


user_cancel = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='🚫 Отмена')]],
        resize_keyboard=True,
)

user_file = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Дальше ▶️')],
                  [KeyboardButton(text='🚫 Отмена')]],
        resize_keyboard=True,
)

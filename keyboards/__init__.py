from .reply.user_keyboard import main_user_keyboard, user_cancel,user_file
from .inline.user_keyboard import content_selection
from .reply.admin_keyboard import main_admin_keyboard, admin_cancel

__all__ = (

    # Клавиатуры пользователей
    "main_user_keyboard",
    "user_cancel",
    "user_file",
    "content_selection",

    # Клавиатуры администраторов
    "main_admin_keyboard",
    "admin_cancel"
)

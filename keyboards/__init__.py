from .reply.user_keyboard import main_user_keyboard, user_cancel, user_file, user_file_2, preview_keyboard, user_back
from .inline.user_keyboard import content_selection
from .reply.admin_keyboard import main_admin_keyboard, admin_cancel, moderation_keyboard, admin_file, admin_back

__all__ = (

    # Клавиатуры пользователей
    "main_user_keyboard",
    "user_cancel",
    "user_file",
    "user_file_2",
    "content_selection",
    "preview_keyboard",
    "user_back",

    # Клавиатуры администраторов
    "main_admin_keyboard",
    "admin_cancel",
    "moderation_keyboard",
    "admin_file",
    "admin_back"
)

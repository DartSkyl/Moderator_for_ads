from keyboards.user_keyboard import (main_user_keyboard, user_cancel, user_file,
                                     user_file_2, preview_keyboard, user_back, user_no_time)
from keyboards.admin_keyboard import (main_admin_keyboard, admin_cancel,
                                      moderation_keyboard, admin_file, admin_back,
                                      view_queue, edit_public_keyboard, admin_back_2, admin_file_2,
                                      admin_preview_keyboard, admin_no_time,
                                      confirm, admin_create_file)

__all__ = (

    # Клавиатуры пользователей
    "main_user_keyboard",
    "user_cancel",
    "user_file",
    "user_file_2",
    "preview_keyboard",
    "user_back",
    "user_no_time",

    # Клавиатуры администраторов
    "main_admin_keyboard",
    "admin_cancel",
    "moderation_keyboard",
    "admin_file",
    "admin_back",
    "view_queue",
    "edit_public_keyboard",
    "admin_back_2",
    "admin_file_2",
    "admin_preview_keyboard",
    "confirm",
    "admin_create_file",
    "admin_no_time"
)

from aiogram.fsm.state import StatesGroup, State


class ModerationAds(StatesGroup):
    """Набор стэйтов для модерации объявлений"""

    # Набор стэйтов для модерации объявления
    mod_preview = State()
    mod_text = State()
    mod_mediafile = State()
    mod_time_for_publication = State()
    mod_validity = State()
    mod_refuse = State()

    # Набор стэйтов для просмотра очереди на публикацию
    pub_preview = State()
    pub_text = State()
    pub_mediafile = State()
    pub_time_for_publication = State()
    pub_validity = State()
    pub_delete = State()

    # Для управления каналами
    add_channel = State()
    remove_channel = State()


class AdminCreated(StatesGroup):
    # Стэйты для создания объявления
    start_creating = State()
    adding_text = State()
    false_state = State()
    adding_mediafile = State()
    time_for_publication = State()
    channel_choice = State()
    preview = State()

    # Стэйты для редактирования
    edit_text = State()
    edit_mediafile = State()
    edit_channel_choice = State()
    edit_time_for_publication = State()

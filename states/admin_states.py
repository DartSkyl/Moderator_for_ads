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

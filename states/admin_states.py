from aiogram.fsm.state import StatesGroup, State


class ModerationAds(StatesGroup):
    """Набор стэйтов для модерации объявлений"""
    # Набор стэйтов для модерации объявления
    mod_preview = State()
    mod_text = State()
    mod_mediafile = State()
    mod_time_for_publication = State()
    mod_validity = State()

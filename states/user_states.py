from aiogram.fsm.state import StatesGroup, State


class CreatingAds(StatesGroup):
    """Набор стэйтов для создания объявления со стороны пользователя"""
    start_creating = State()
    adding_text = State()
    false_state = State()
    adding_mediafile = State()
    time_for_publication = State()
    validity = State()

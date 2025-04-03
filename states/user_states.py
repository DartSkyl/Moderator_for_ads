from aiogram.fsm.state import StatesGroup, State


class CreatingAds(StatesGroup):
    """Набор стэйтов для создания объявления со стороны пользователя"""
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
    edit_time_for_publication = State()
    edit_channel_choice = State()

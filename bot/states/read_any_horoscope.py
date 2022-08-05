from aiogram.dispatcher.filters.state import StatesGroup, State


class ReadAnyHoroscope(StatesGroup):
    zodiac_sign_chosen = State()
    time_period_chosen = State()

from aiogram.dispatcher.filters.state import StatesGroup, State


class SetZodiacSign(StatesGroup):
    self_zodiac_sign_chosen = State()

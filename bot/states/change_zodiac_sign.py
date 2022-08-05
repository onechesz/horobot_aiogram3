from aiogram.dispatcher.filters.state import StatesGroup, State


class ChangeZodiacSign(StatesGroup):
    new_zodiac_sign_chosen = State()

__all__ = ['register_message_handlers']

from aiogram import Dispatcher

from .change_zodiac_sign import register as change_zodiac_sign_register
from .horoscope_daily import register as horoscope_daily_register
from .horoscope_tomorrow import register as horoscope_tomorrow_register
from .horoscope_weekly import register as horoscope_weekly_register
from .read_any_horoscope import register as read_any_horoscope_register
from .set_zodiac_sign import register as set_zodiac_sign_register


def register_message_handlers(dispatcher: Dispatcher) -> None:
    set_zodiac_sign_register(dispatcher)
    read_any_horoscope_register(dispatcher)
    change_zodiac_sign_register(dispatcher)
    horoscope_daily_register(dispatcher)
    horoscope_tomorrow_register(dispatcher)
    horoscope_weekly_register(dispatcher)

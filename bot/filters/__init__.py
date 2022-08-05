__all__ = ['register_message_filters', 'IsZodiacSign', 'IsTimePeriod']

from aiogram import Dispatcher

from .zodiac_signs import IsZodiacSign
from .time_periods import IsTimePeriod


def register_message_filters(dispatcher: Dispatcher) -> None:
    pass

from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message


class IsTimePeriod(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        zodiac_signs_or_cancel = [
            'Гороскоп на сегодня',
            'Гороскоп на завтра',
            'Гороскоп на неделю',
            'Отмена'
        ]

        return message.text in zodiac_signs_or_cancel

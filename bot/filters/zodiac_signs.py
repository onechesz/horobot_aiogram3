from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message


class IsZodiacSign(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        zodiac_signs_or_cancel = [
            'Овен',
            'Телец',
            'Близнецы',
            'Рак',
            'Лев',
            'Дева',
            'Весы',
            'Скорпион',
            'Стрелец',
            'Козерог',
            'Водолей',
            'Рыбы',
            'Отмена'
        ]

        return message.text in zodiac_signs_or_cancel

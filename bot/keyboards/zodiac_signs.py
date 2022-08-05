from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def zodiac_signs_k():
    zodiac_signs_keyboard = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text='Овен'),
            KeyboardButton(text='Телец'),
            KeyboardButton(text='Близнецы')
        ],
        [
            KeyboardButton(text='Рак'),
            KeyboardButton(text='Лев'),
            KeyboardButton(text='Дева')
        ],
        [
            KeyboardButton(text='Весы'),
            KeyboardButton(text='Скорпион'),
            KeyboardButton(text='Стрелец')
        ],
        [
            KeyboardButton(text='Козерог'),
            KeyboardButton(text='Водолей'),
            KeyboardButton(text='Рыбы')
        ],
        [KeyboardButton(text='Отмена')]
    ], resize_keyboard=True)

    return zodiac_signs_keyboard

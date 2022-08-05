from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def time_periods_k():
    time_periods_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Гороскоп на сегодня')],
        [KeyboardButton(text='Гороскоп на завтра')],
        [KeyboardButton(text='Гороскоп на неделю')],
        [KeyboardButton(text='Отмена')]
    ], resize_keyboard=True)

    return time_periods_keyboard

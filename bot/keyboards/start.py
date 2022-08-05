from aiogram.types.keyboard_button import KeyboardButton
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup


def start_unregistered_k():
    start_unregistered_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Указать свой знак зодиака')],
        [KeyboardButton(text='Посмотреть гороскоп по всем знакам зодиака')]
    ], resize_keyboard=True)

    return start_unregistered_keyboard


def start_registered_k():
    start_registered_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Изменить свой знак зодиака')],
        [
            KeyboardButton(text='Гороскоп на сегодня'),
            KeyboardButton(text='Гороскоп на завтра'),
            KeyboardButton(text='Гороскоп на неделю')
        ],
        [KeyboardButton(text='Посмотреть гороскоп по всем знакам зодиака')]
    ], resize_keyboard=True)

    return start_registered_keyboard

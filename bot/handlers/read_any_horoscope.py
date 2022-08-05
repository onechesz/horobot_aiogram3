import asyncio

from aiogram import Dispatcher, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Horoscope, Users
from bot.filters import IsZodiacSign, IsTimePeriod
from bot.keyboards import zodiac_signs_k, start_unregistered_k, start_registered_k, time_periods_k
from bot.states import ReadAnyHoroscope


async def read_any_horoscope_m(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, выберите <b>знак зодиака</b>, для которого Вы'
                              'хотите посмотреть гороскоп, <b>из предложенных</b>.\n'
                              'Действие можно отменить <i>соответствующей кнопкой</i>.',
                         reply_markup=zodiac_signs_k())
    await state.set_state(ReadAnyHoroscope.zodiac_sign_chosen)


async def zodiac_sign_m(message: Message, state: FSMContext, session_maker: sessionmaker):
    chosen_zodiac_sign = message.text

    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session.execute(select(Users.zodiac_sign)
                                                         .where(Users.user_id == message.from_user.id))
            user: Users = result.one_or_none()[0]

            if user:
                reply_keyboard_markup = start_registered_k()
            else:
                reply_keyboard_markup = start_unregistered_k()

    if chosen_zodiac_sign == 'Отмена':
        await message.answer(text='Чего бы Вы хотели?', reply_markup=reply_keyboard_markup)
        await state.clear()
    else:
        await message.answer(text='Пожалуйста, выберите <b>период времени</b>, на который Вы'
                                  'хотите посмотреть гороскоп, из <b>предложенных</b>.\n'
                                  'Действие можно отменить <i>соответствующей кнопкой</i>.',
                             reply_markup=time_periods_k())
        await state.update_data(zodiac_sign=chosen_zodiac_sign, reply_keyboard_markup=reply_keyboard_markup)
        await state.set_state(ReadAnyHoroscope.time_period_chosen)


async def time_period_m(message: Message, state: FSMContext, session_maker: sessionmaker):
    chosen_time_period = message.text

    if chosen_time_period == 'Отмена':
        user_data = await state.get_data()
        reply_keyboard_markup = user_data['reply_keyboard_markup']

        await message.answer(text='Чего бы Вы хотели?', reply_markup=reply_keyboard_markup)
        await state.clear()
    else:
        user_data = await state.get_data()
        chosen_zodiac_sign = user_data['zodiac_sign']

        if chosen_time_period == 'Гороскоп на сегодня':
            db_time_period = Horoscope.horoscope_daily
        elif chosen_time_period == 'Гороскоп на завтра':
            db_time_period = Horoscope.horoscope_tomorrow
        else:
            db_time_period = Horoscope.horoscope_weekly

        session: AsyncSession

        async with session_maker() as session:
            async with session.begin():
                result: ScalarResult = await session.execute(select(db_time_period)
                                                             .where(Horoscope.zodiac_sign == chosen_zodiac_sign))
                horoscope: Horoscope = result.one_or_none()[0]

        await message.answer(text=f'<b>{chosen_zodiac_sign}</b> — {chosen_time_period.lower()}:\n'
                                  f'<i>{horoscope}</i>', reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(1)
        await message.answer(text='Чего бы Вы хотели ещё?', reply_markup=user_data['reply_keyboard_markup'])
        await state.clear()


def register(dispatcher: Dispatcher):
    dispatcher.message.register(read_any_horoscope_m, F.text == 'Посмотреть гороскоп по всем знакам зодиака')
    dispatcher.message.register(zodiac_sign_m, IsZodiacSign(), state=ReadAnyHoroscope.zodiac_sign_chosen)
    dispatcher.message.register(time_period_m, IsTimePeriod(), state=ReadAnyHoroscope.time_period_chosen)

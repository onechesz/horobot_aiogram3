from aiogram import Dispatcher, F
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Users, Horoscope


async def horoscope_daily_m(message: Message, session_maker: sessionmaker):
    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session.execute(select(Users.zodiac_sign)
                                                         .where(Users.user_id == message.from_user.id))
            user_zodiac_sign: Users = result.one_or_none()[0]

    if not user_zodiac_sign:
        return await message.answer(text='Вы <b>не можете</b> узнать личный гороскоп, так как <b>ещё не указали</b> '
                                         'собственный знак зодиака.')

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session.execute(select(Horoscope.horoscope_daily)
                                                         .where(Horoscope.zodiac_sign == user_zodiac_sign))
            horoscope: Horoscope = result.one_or_none()[0]

    await message.answer(text=f'Ваш <b>личный</b> {message.text.lower()} (<b>{user_zodiac_sign.lower()}</b>):\n'
                              f'<i>{horoscope}</i>')


def register(dispatcher: Dispatcher):
    dispatcher.message.register(horoscope_daily_m, F.text == 'Гороскоп на сегодня', state=None)

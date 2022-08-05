from aiogram import Dispatcher, F
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import update, select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Users
from bot.filters import IsZodiacSign
from bot.keyboards import zodiac_signs_k, start_registered_k
from bot.states import ChangeZodiacSign


async def change_zodiac_sign_m(message: Message, state: FSMContext, session_maker: sessionmaker):
    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session.execute(select(Users.zodiac_sign)
                                                         .where(Users.user_id == message.from_user.id))
            user: Users = result.one_or_none()[0]

    if not user:
        return await message.answer(text='Вы не можете <b>изменить</b> свой знак зодиака, поскольку '
                                         '<b>ещё не указали</b> его.')

    await message.answer(text='Пожалуйста, выберите <b>Ваш знак зодиака</b> из <b>предложенных</b>.\n'
                              'Действие можно отменить <i>соответствующей кнопкой</i>.',
                         reply_markup=zodiac_signs_k())
    await state.set_state(ChangeZodiacSign.new_zodiac_sign_chosen)


async def zodiac_sign_m(message: Message, state: FSMContext, session_maker: sessionmaker):
    chosen_zodiac_sign = message.text

    if chosen_zodiac_sign == 'Отмена':
        await message.answer(text='Чего бы Вы хотели?', reply_markup=start_registered_k())
    else:
        session: AsyncSession

        async with session_maker() as session:
            async with session.begin():
                await session.execute(update(Users).where(Users.user_id == message.from_user.id)
                                      .values(zodiac_sign=chosen_zodiac_sign))

        await message.answer(text='Вы <b>успешно</b> сохранили свой знак зодиака.', reply_markup=start_registered_k())

    await state.clear()


def register(dispatcher: Dispatcher):
    dispatcher.message.register(change_zodiac_sign_m, F.text == 'Изменить свой знак зодиака')
    dispatcher.message.register(zodiac_sign_m, IsZodiacSign(), state=ChangeZodiacSign.new_zodiac_sign_chosen)

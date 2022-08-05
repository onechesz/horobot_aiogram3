from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Users
from bot.keyboards import start_unregistered_k, start_registered_k


async def start_c(message: Message, session_maker: sessionmaker) -> None:
    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session.execute(select(Users.zodiac_sign).where(
                Users.user_id == message.from_user.id))
            zodiac_sign: Users = result.one_or_none()[0]

    if zodiac_sign:
        reply_keyboard_markup = start_registered_k()
    else:
        reply_keyboard_markup = start_unregistered_k()

    await message.answer(text='<b>Здравствуйте.</b>\nЧего бы Вы хотели?', reply_markup=reply_keyboard_markup)

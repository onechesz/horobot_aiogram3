import asyncio

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Horoscope, Users


async def users_notification_sch(session_maker: sessionmaker, bot: Bot):
    session: AsyncSession

    async with session_maker() as session:
        async with session.begin():
            result: ScalarResult = await session \
                .execute(select(Users.user_id, Users.zodiac_sign, Horoscope.horoscope_daily)
                         .join(Horoscope, Users.zodiac_sign == Horoscope.zodiac_sign))
            users: Users = result.all()

    async def users_notification(user_id, zodiac_sign, horoscope):
        await bot.send_message(chat_id=user_id,
                               text=f'<b>Доброе утро.</b>\n\n'
                                    f'Ваш гороскоп на сегодня (<b>{zodiac_sign.lower()}</b>):\n'
                                    f'<i>{horoscope}</i>')

    coroutines = [users_notification(tup[0], tup[1], tup[2]) for tup in users]

    await asyncio.gather(*coroutines)


def register(scheduler: AsyncIOScheduler, session_maker: sessionmaker, bot: Bot):
    scheduler.add_job(users_notification_sch, 'cron', hour=9, args=(session_maker, bot))
    # scheduler.add_job(users_notification_sch, 'interval', seconds=3, args=(session_maker, bot))

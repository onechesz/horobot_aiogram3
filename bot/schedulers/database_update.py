import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Horoscope
from bot.parsers import horoscope_daily, horoscope_tomorrow, horoscope_weekly


async def database_update_sch(session_maker: sessionmaker):
    async def db_update_daily(key, value, period):
        session: AsyncSession

        async with session_maker() as session:
            async with session.begin():
                await session.execute(update(Horoscope).where(Horoscope.zodiac_sign == key)
                                      .values({period: value}))

    coroutines = [db_update_daily(key, value, 'horoscope_daily') for key, value in horoscope_daily.items()]
    coroutines.extend([db_update_daily(key, value, 'horoscope_tomorrow') for key, value in horoscope_tomorrow.items()])
    coroutines.extend([db_update_daily(key, value, 'horoscope_weekly') for key, value in horoscope_weekly.items()])

    await asyncio.gather(*coroutines)


def register(scheduler: AsyncIOScheduler, session_maker: sessionmaker):
    scheduler.add_job(database_update_sch, 'cron', hour=6, args=(session_maker,))
    # scheduler.add_job(database_update_sch, 'interval', seconds=3, args=(session_maker,))

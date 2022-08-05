__all__ = ['register_schedulers']

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import sessionmaker

from .database_update import register as database_update_register
from .user_notification import register as users_notification_register


def register_schedulers(scheduler: AsyncIOScheduler, session_maker: sessionmaker, bot: Bot):
    database_update_register(scheduler, session_maker)
    users_notification_register(scheduler, session_maker, bot)

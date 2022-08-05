import asyncio
import logging
import os

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.engine import URL

from bot.middlewares import UserCheck
from commands import register_user_commands
from commands.command_list import bot_commands
from database import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from filters import register_message_filters
from handlers import register_message_handlers
from bot.schedulers import register_schedulers


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = list()

    for command in bot_commands:
        commands_for_bot.append(BotCommand(command=command[0], description=command[1]))

    dispatcher = Dispatcher()
    bot = Bot(
        token=os.getenv('token'),
        parse_mode='HTML'
    )
    postgres_url = URL.create(
        drivername='postgresql+asyncpg',
        username=os.getenv('db_user'),
        port=os.getenv('db_port'),
        host='localhost',
        password=os.getenv('db_password'),
        database=os.getenv('db_name')
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    scheduler = AsyncIOScheduler()

    await bot.set_my_commands(commands=commands_for_bot)

    dispatcher.message.middleware(UserCheck())
    register_message_filters(dispatcher)
    register_user_commands(dispatcher)
    register_message_handlers(dispatcher)
    register_schedulers(scheduler, session_maker, bot)

    scheduler.start()
    await proceed_schemas(async_engine, BaseModel.metadata)
    await dispatcher.start_polling(bot, session_maker=session_maker)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')

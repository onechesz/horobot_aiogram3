from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from bot.database import Users


class UserCheck(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message,
                       data: Dict[str, Any]) -> Any:
        session_maker: sessionmaker = data['session_maker']
        session: AsyncSession

        async with session_maker() as session:
            async with session.begin():
                result: ScalarResult = await session.execute(select(Users).where(Users.user_id == event.from_user.id))
                user: Users = result.one_or_none()

                if user:
                    pass
                else:
                    user = Users(user_id=event.from_user.id)

                    await session.merge(user)

        return await handler(event, data)

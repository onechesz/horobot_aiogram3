__all__ = ['register_user_commands']

from aiogram import Router
from aiogram.dispatcher.filters.command import CommandStart

from .start import start_c


def register_user_commands(router: Router) -> None:
    router.message.register(start_c, CommandStart())

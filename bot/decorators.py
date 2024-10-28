import asyncio
from functools import wraps

from aiogram.types import Message
from asgiref.sync import sync_to_async

from section.services.base_section import UserSectionService
from user.services import UserService


def inject_user(handler):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        telegram_id = message.from_user.id
        username = message.from_user.username
        loop = asyncio.get_event_loop()
        user = await loop.run_in_executor(None, UserService.get_or_create_user_by_telegram_id, telegram_id, username)
        return await handler(message, user=user, *args, **kwargs)
    return wrapper

def inject_base_section(handler):
    @wraps(handler)
    async def wrapper(message: Message, user, *args, **kwargs):
        loop = asyncio.get_event_loop()
        base_section = await loop.run_in_executor(None, UserSectionService.get_or_create_base_section_for_user, user)
        return await handler(message, user=user, base_section=base_section, *args, **kwargs)
    return wrapper
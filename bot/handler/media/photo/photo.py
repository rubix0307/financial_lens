import asyncio

from aiogram import F, types
from aiogram.enums import ContentType
from django.contrib.auth import get_user_model

from bot.apps import bot
from bot.common import save_message_media
from bot.decorators import inject_base_section, inject_user
from bot.managers import ChatActionManager
from bot.service import BotService
from section.models import Section


User = get_user_model()

@bot.dp.message(F.content_type == ContentType.PHOTO)
@inject_user
@inject_base_section
async def start_command(
        message: types.Message,
        user: User,
        base_section: Section,
    ):
    async with ChatActionManager(bot.bot, chat_id=message.chat.id, delay=5):
        saved_media = await save_message_media(message)

        loop = asyncio.get_running_loop()
        receipt, products = await loop.run_in_executor(
            None,
            BotService.analyze_and_save_receipt,
            saved_media, user, base_section
        )

        await message.reply(str(receipt))

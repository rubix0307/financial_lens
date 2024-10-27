import asyncio

from aiogram import F, types
from aiogram.enums import ContentType
from django.contrib.auth import get_user_model

from bot.apps import bot
from bot.common import save_message_media
from bot.managers import ChatActionManager
from bot.service import BotService
from section.models import Section

User = get_user_model()

@bot.dp.message(F.content_type == ContentType.PHOTO)
async def start_command(
        message: types.Message,
        user: User = None,
        active_section: Section = None
    ):
    async with ChatActionManager(bot.bot, chat_id=message.chat.id, delay=5):
        saved_media = await save_message_media(message)
        user = await User.objects.aget(username='root')

        loop = asyncio.get_running_loop()
        receipt, products = await loop.run_in_executor(
            None,
            BotService.analyze_and_save_receipt,
            saved_media, user, active_section
        )

        await message.reply(str(receipt))

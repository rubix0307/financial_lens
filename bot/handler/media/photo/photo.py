from aiogram import F, types
from aiogram.enums import ContentType

from bot.apps import bot


@bot.dp.message(F.content_type == ContentType.PHOTO)
async def start_command(message: types.Message):
    await message.reply("photo")
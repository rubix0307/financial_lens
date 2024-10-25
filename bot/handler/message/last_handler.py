from aiogram import types
from bot.apps import bot


@bot.dp.message()
async def last_handler(message: types.Message):
    await message.reply("Your request cannot be sent for processing")
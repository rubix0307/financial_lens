from aiogram import types
from aiogram.filters import Command
from bot.apps import bot


@bot.dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.reply("welcome")

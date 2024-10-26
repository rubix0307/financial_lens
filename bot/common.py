import os
from dataclasses import dataclass

from aiogram import types
from django.conf import settings
from .apps import bot


@dataclass
class SavedMedia:
    image_name: str
    image_path: str
    saved_file: str


async def save_message_media(message: types.Message):
    if message.photo:
        image_name = f"{message.chat.id}_{message.photo[-1].file_id}.jpg"
        image_path = os.path.join(settings.TELEGRAM_MEDIA_PATH, image_name)
        file = message.photo[-1]
    else:
        return

    saved_file = await bot.bot.download(file, destination=image_path)
    return SavedMedia(image_name, image_path, saved_file)
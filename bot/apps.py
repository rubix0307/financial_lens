import os
import threading
from django.apps import AppConfig
from .runner import SingletonBot

bot = SingletonBot()

class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true':
            from bot.handler import bot
            threading.Thread(target=bot.start_bot, daemon=True).start()
import asyncio
from aiogram import Bot, Dispatcher
from django.conf import settings


class SingletonBot:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonBot, cls).__new__(cls)
            cls._instance.bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
            cls._instance.dp = Dispatcher()
            cls._instance.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(cls._instance.loop)
        return cls._instance

    async def set_webhook(self):
        await self.bot.set_webhook(settings.TELEGRAM_WEBHOOK_URL)


    def start_bot(self):
        self.loop.run_until_complete(self.set_webhook())
        self.loop.run_forever()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from aiogram.types import Update
from .runner import SingletonBot

bot_client = SingletonBot()


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        json_str = request.body.decode('UTF-8')
        update = Update.parse_raw(json_str)
        bot_client.loop.run_in_executor(
            None,
            lambda: bot_client.loop.create_task(bot_client.dp.feed_update(bot_client.bot, update))
        )
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'forbidden'})



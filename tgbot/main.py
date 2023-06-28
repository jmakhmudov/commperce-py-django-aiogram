import logging
import os

import django

logging.basicConfig(level=logging.INFO)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()

import asyncio

from aiogram.utils import executor

from app.bot import dp
from app.bot.handlers.auto import send_publication
from bot_settings import elastic, elastic_params


async def on_startup(dp):
    if not elastic.indices.exists("check"):
        elastic.indices.create(index="check", body=elastic_params)
    loop = asyncio.get_event_loop()
    loop.create_task(send_publication())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

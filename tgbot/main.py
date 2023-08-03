import logging
import os

import django
import aiohttp
import time

logging.basicConfig(level=logging.INFO)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup()

def check_migrations():
    from bot_settings import get_active_settings
    logging.info("There are pending migrations. Waiting for migrations to be applied...")
    while True:
        try:
            get_active_settings()
            logging.info("All migrations have been applied.")
            return
        except django.db.utils.ProgrammingError:
            logging.info('do not ready')
            time.sleep(2)
check_migrations()


import asyncio

from aiogram.utils import executor

from app.bot import dp
from app.bot.handlers.auto import send_publication
from bot_settings import elastic, elastic_params, get_active_settings


async def on_startup(dp):
    if not elastic.indices.exists("check"):
        elastic.indices.create(index="check", body=elastic_params)
    loop = asyncio.get_event_loop()
    loop.create_task(send_publication())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

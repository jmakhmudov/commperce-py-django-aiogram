import datetime
import logging
import os
from asyncio import sleep

import pytz
from aiogram import types

from app.bot.container import filter_service
from app.bot.filters.base import IsAllowedGroup, IsNotChatAdmin
from app.bot.loader import bot, dp
from bot_settings import check_publications


@dp.message_handler(IsAllowedGroup(), IsNotChatAdmin())
async def chat_filtering(message: types.Message):
    try:
        need_to_delete, text, wait = filter_service.need_to_delete(message)
        if need_to_delete:
            await message.delete()
            ans_text = await bot.send_message(
                chat_id=message.chat.id,
                text=text,
            )
            await sleep(wait)
            await ans_text.delete()
    except Exception as e:
        logging.info(e)


async def send_publication():
    tz = pytz.timezone("Europe/Moscow")
    while True:
        plans = await check_publications()
        for plan in plans:
            if plan.publ_at <= datetime.datetime.now(tz=tz):
                if plan.image:
                    photo = types.InputFile(path_or_bytesio=plan.image.path)
                    await bot.send_photo(
                        chat_id=plan.group.tgid, photo=photo, caption=plan.body
                    )
                    os.remove(plan.image.path)
                else:
                    await bot.send_message(chat_id=plan.group.tgid, text=plan.body)

                plan.delete()

        await sleep(60)

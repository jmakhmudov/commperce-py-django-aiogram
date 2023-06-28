import logging
from asyncio import sleep

from aiogram import types
from aiogram.dispatcher.filters import Command

from app.bot.filters.base import IsAllowedGroup, IsBoss, IsChatAdmin, IsGroup
from app.bot.loader import bot, dp
from app.bot.secondary.text import mute_restrict_text, unmute_restrict_text
from app.models import Group
from app.services import ManageService
from bot_settings import get_active_settings


@dp.message_handler(IsBoss(), IsGroup(), Command(["activate"], prefixes="!/"))
async def activate_chat(message: types.Message):
    try:
        Group.objects.update_or_create(
            tgid=message.chat.id, defaults={"name": message.chat.full_name}
        )
        ans_text = await message.answer(text="Чат активирован")
        await sleep(30)
        await ans_text.delete()
    except Exception as e:
        logging.info(e)


@dp.message_handler(
    IsAllowedGroup(), IsChatAdmin(), Command(["ban", "бан"], prefixes="!/")
)
async def ban_member_manage(message: types.Message):
    try:
        member = message.reply_to_message.from_user
        await bot.ban_chat_member(chat_id=message.chat.id, user_id=member.id)
        await message.delete()
    except Exception as e:
        logging.info(e)


@dp.message_handler(
    IsAllowedGroup(), IsChatAdmin(), Command(["mute", "мут"], prefixes="!/")
)
async def mute_member_manage(message: types.Message):
    try:
        settings = await get_active_settings(message.chat.id)
        member = message.reply_to_message.from_user
        (
            mute_time,
            permissions,
            comment,
            attribute,
            time,
        ) = ManageService.restrict_member_func(message.text)
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=member.id,
            permissions=permissions,
            until_date=mute_time,
        )
        await message.delete()
        ans_text = await message.answer(
            text=mute_restrict_text(
                admin=message.from_user.get_mention(as_html=True),
                member=member.get_mention(as_html=True),
                comment=comment,
                mute_time=time,
                attribute=attribute,
            )
        )
        await sleep(settings.wait_time)
        await ans_text.delete()
    except Exception as e:
        logging.info(e)


@dp.message_handler(
    IsAllowedGroup(), IsChatAdmin(), Command(["unmute", "размутить"], prefixes="!/")
)
async def unmute_member_manage(message: types.Message):
    try:
        settings = await get_active_settings(message.chat.id)
        member = message.reply_to_message.from_user
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=member.id,
            permissions=types.ChatPermissions(
                can_send_messages=True,
                can_invite_users=True,
                can_send_media_messages=True,
                can_send_photos=True,
            ),
            until_date=0,
        )
        await message.delete()
        ans_text = await message.answer(
            text=unmute_restrict_text(member=member.get_mention(as_html=True))
        )
        await sleep(settings.wait_time)
        await ans_text.delete()
    except Exception as e:
        logging.info(e)

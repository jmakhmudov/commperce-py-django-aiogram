from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from app.bot.loader import bot
from bot_settings import ADMINS, ALLOWED_GROUPS


class IsBoss(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        bosses_id = list(map(lambda boss: boss.tgid, ADMINS))
        return str(message.from_user.id) in bosses_id


class IsGroup(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        return message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)


class IsAllowedGroup(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        allowed_groups_id = list(map(lambda group: group.tgid, ALLOWED_GROUPS))
        return (
            message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)
            and str(message.chat.id) in allowed_groups_id
        )


class IsChatAdmin(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        member = await bot.get_chat_member(
            chat_id=message.chat.id, user_id=message.from_user.id
        )
        return member.is_chat_admin()


class IsNotChatAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await bot.get_chat_member(message.chat.id, message.from_user.id)
        return not member.is_chat_admin()

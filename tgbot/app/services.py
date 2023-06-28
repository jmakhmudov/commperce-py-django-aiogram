import datetime
import re

from aiogram import types

from bot_settings import elastic, get_active_settings


class FilterService:
    settings = get_active_settings()

    def need_to_delete(self, message):
        self.settings = get_active_settings(message.chat.id)
        if self._check_url(message) and self.settings.include_url:
            return True, self.settings.text_url, self.settings.wait_time
        if self._check_shitword(message.text) and self.settings.include_shitword:
            return True, self.settings.text_shitword, self.settings.wait_time
        if self._check_length(message.text) and self.settings.include_length:
            return True, self.settings.text_length, self.settings.wait_time

        return False, None, None

    def _check_url(self, message):
        for entity in message.entities:
            if entity.type in (
                types.MessageEntityType.URL,
                types.MessageEntityType.TEXT_LINK,
            ):
                return True

    def _check_shitword(self, text):
        shitwords = self.settings.shitwords
        doc = {"text": text}
        elastic.index(index="check", id=1, body=doc, refresh=True)
        for word in shitwords.split(", "):
            query = {
                "query": {
                    "match": {
                        "text": {
                            "query": word,
                            "fuzziness": "AUTO",
                            "operator": "and",
                        }
                    }
                }
            }
            result = elastic.search(index="check", body=query)
            if result["hits"]["total"]["value"]:
                return True

    def _check_length(self, text):
        return len(text) > self.settings.max_length


class ManageService:
    @staticmethod
    def restrict_member_func(message):
        command = re.compile(r"[!/](mute|мут) ?(\d+)?([smhdw])? ?([\w+\W]+)?")
        parsed = command.match(message)
        time = parsed.group(2)
        attribute = parsed.group(3)
        comment = parsed.group(4)
        if not time:
            time = 5
        else:
            time = int(time)
        if attribute == "s":
            mute_time = datetime.datetime.now() + datetime.timedelta(seconds=time)
        elif attribute == "m":
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=time)
        elif attribute == "h":
            mute_time = datetime.datetime.now() + datetime.timedelta(hours=time)
        elif attribute == "d":
            mute_time = datetime.datetime.now() + datetime.timedelta(days=time)
        elif attribute == "w":
            mute_time = datetime.datetime.now() + datetime.timedelta(weeks=time)
        elif attribute is None:
            attribute = "m"
            mute_time = datetime.datetime.now() + datetime.timedelta(minutes=time)
        else:
            return False
        permissions = types.ChatPermissions(
            can_send_messages=False,
            can_invite_users=False,
            can_send_media_messages=False,
            can_send_photos=False,
        )

        return mute_time, permissions, comment, attribute, time

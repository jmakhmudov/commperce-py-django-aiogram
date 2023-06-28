from aiogram import Bot, Dispatcher, types

from bot_settings import API_TOKEN

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot=bot)

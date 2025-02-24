from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from telellm.lib.config import BOT_TOKEN, MODEL_NAME

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot_name: str = None
model_name: str = MODEL_NAME


def set_bot_name(name: str):
    global bot_name
    bot_name = name


def get_model_name():
    global model_name
    return model_name


def set_model_name(value):
    global model_name
    model_name = value

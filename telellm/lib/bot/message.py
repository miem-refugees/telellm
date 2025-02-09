from aiogram import Router
from aiogram.types import Message

from .bot import bot_name, bot
from .ollama import ollama_request
from .auth import auth
from .thread import collect_message_thread, format_thread_for_prompt

message_router = Router()


@message_router.message()
@auth
async def message_handler(message: Message):
    if message.chat.type == "private":
        prompt = message.text or message.caption
        await ollama_request(message, prompt)
    elif message.chat.type in {"group", "supergroup"} and is_mention_or_reply(message):
        thread = await collect_message_thread(message)
        prompt = format_thread_for_prompt(thread)

        await ollama_request(message, prompt)


async def is_mention_or_reply(message: Message):
    is_mentioned = (message.text and message.text.startswith(bot_name)) or (
        message.caption and message.caption.startswith(bot_name)
    )

    is_reply_to_bot = (
        message.reply_to_message and message.reply_to_message.from_user.id == bot.id
    )

    return is_mentioned or is_reply_to_bot

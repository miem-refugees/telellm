from aiogram.types import Message
from .bot import bot


async def collect_message_thread(message: Message, thread=None):
    if thread is None:
        thread = []

    thread.insert(0, message)

    if message.reply_to_message:
        await collect_message_thread(message.reply_to_message, thread)

    return thread


def format_thread_for_prompt(thread):
    prompt = "Conversation thread:\n\n"
    for msg in thread:
        sender = "User" if msg.from_user.id != bot.id else "Bot"
        content = msg.text or msg.caption or "[No text content]"
        prompt += f"{sender}: {content}\n\n"

    prompt += "History:"
    return prompt

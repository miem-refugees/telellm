from functools import wraps
from aiogram.types import Message, CallbackQuery

from telellm.lib.config import CHAT_IDS, USER_IDS


def auth(func):
    @wraps(func)
    async def wrapper(message: Message = None, query: CallbackQuery = None):
        user_id = message.from_user.id if message else query.from_user.id
        chat_id = message.chat.id if message else query.from_user.id
        if user_id in USER_IDS or chat_id in CHAT_IDS:
            if message:
                return await func(message)
            elif query:
                return await func(query=query)

    return wrapper

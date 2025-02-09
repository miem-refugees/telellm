from asyncio.locks import Lock

from aiogram.types import Message


class INMemoryContext:
    def __init__(self):
        self.mem = dict()
        self.rwlock = Lock()

    def get(self, message: Message, default=None) -> dict | None:
        return self.mem.get(message.chat.id, default)

    async def set(self, message: Message, value):
        async with self.rwlock:
            self.mem[message.chat.id] = value

    async def append_context(self, message: Message, event: dict):
        async with self.rwlock:
            self.mem[message.chat.id]["messages"].append(event)

    async def reset(self, key):
        async with self.rwlock:
            self.mem.pop(key, None)

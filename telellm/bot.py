from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from lib.bot import bot_system_router


class TelegramBot:
    def __init__(self, token: str):
        self.bot = Bot(
            token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()

        dp.include_routers(
            bot_system_router,
        )

        self.dp = dp

    async def start_polling(self):
        await self.dp.start_polling(self.bot)

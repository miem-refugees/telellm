from asyncio import run
from aiogram import Dispatcher
from logger import init_logger

from telellm.lib.bot import init_bot
from telellm.lib.bot.commands import command_router
from telellm.lib.bot.message import message_router


async def main():
    init_logger()
    bot = await init_bot()

    dp = Dispatcher()
    dp.include_routers(
        command_router,
        message_router,
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())

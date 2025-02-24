import asyncio

from aiogram import Dispatcher

from telellm.lib.bot import bot, set_bot_name
from telellm.lib.logger import init_logger
from telellm.lib.bot.callback import callback_router
from telellm.lib.bot.commands import command_router, update_bot_commands
from telellm.lib.bot.message import message_router


async def main():
    init_logger()

    dp = Dispatcher()
    dp.include_routers(
        callback_router,
        command_router,
        message_router,
    )

    bot_me = await bot.get_me()
    set_bot_name(f"@{bot_me.username}")
    await update_bot_commands()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

from loguru import logger
from asyncio import run
from aiogram import Dispatcher
from logger import init_logger

from telellm.lib.bot import bot, llm, set_bot_name, get_model_name
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
    logger.debug("updated bot commands")

    init_model_name = get_model_name()
    logger.debug("Pulling model: {}", init_model_name)
    await llm.pull(init_model_name)
    logger.debug("Pulled model: {}", init_model_name)

    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())

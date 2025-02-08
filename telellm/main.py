import os
import asyncio

from aiogram.enums import ParseMode
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from lib.ollama import Ollama
from lib.bot import LLMManager, bot_system_router, create_message_router
from logger import init_logger


async def main():
    load_dotenv()
    init_logger()

    token = os.getenv("TOKEN")
    if token is None:
        raise RuntimeError("TOKEN is not set")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    ollama_host = os.getenv("OLLAMA_HOST")
    ollama_port = os.getenv("OLLAMA_PORT")
    if ollama_host is None or ollama_port is None:
        raise RuntimeError("OLLAMA_HOST or OLLAMA_PORT is not set")

    llm_manager = LLMManager(bot, Ollama(ollama_host, int(ollama_port)))

    dp = Dispatcher()
    dp.include_routers(bot_system_router, create_message_router(llm_manager))

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
